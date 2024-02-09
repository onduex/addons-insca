# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from operator import itemgetter
from itertools import groupby

all_components = []
all_lines = []


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    product_name = fields.Char(string='Nombre', related='product_tmpl_id.name', store=True)
    product_default_code = fields.Char(string='Referencia', related='product_tmpl_id.default_code', store=True)
    product_tmpl_id = fields.Many2one(tracking=1)
    product_qty = fields.Float(tracking=1)
    bom_line_ids = fields.One2many(tracking=1)
    fecha_solicitud = fields.Date(string='Fecha solicitud', required=False, tracking=1)
    fecha_recepcion = fields.Date(string='Fecha recepción', required=False, tracking=1)
    fecha_recogido = fields.Date(string='Fecha recogido', required=False, tracking=1)
    fecha_entrega_cliente = fields.Date(string='Fecha entrega cliente', required=False, tracking=1)
    cliente = fields.Many2one(comodel_name='res.partner', string='Cliente', required=False, tracking=1)
    cliente_ref = fields.Char(string='Referencia cliente', required=False, tracking=1, related='cliente.ref')
    trabajo = fields.Many2one(comodel_name='project.project', string='Trabajo', required=False, tracking=1)
    emitido = fields.Many2one(comodel_name='hr.employee', string='Emitido por', required=False, tracking=1)
    preparado = fields.Many2one(comodel_name='hr.employee', string='Preparado por', required=False, tracking=1)
    recogido = fields.Many2one(comodel_name='hr.employee', string='Recogido por', required=False, tracking=1)
    observaciones = fields.Text(string="Observaciones", required=False, tracking=1)
    codigo_plano = fields.Char(string='Código de Plano', required=False, tracking=1)
    n_cee = fields.Char(string='Nº CEE', required=False, tracking=1)
    seccion = fields.Many2one(comodel_name="seccion", string="Sección", required=False, store=True, tracking=1)
    secciones = fields.Many2many(comodel_name="seccion",
                                 string="Secciones a imprimir",
                                 required=False,
                                 store=True,
                                 default=lambda self: self.env['seccion'].search([]))
    state = fields.Selection(selection=[
        ('ot', 'OT'),
        ('almacen', 'ALMACEN'),
        ('compras', 'COMPRAS'),
        ('montaje', 'MONTAJE'),
        ('completado', 'COMPLETADO'),
    ], string='Etapa', required=True, copy=False, tracking=True, default='ot')
    line_count = fields.Integer(compute='compute_count')

    def get_bom_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Componentes',
            'view_mode': 'tree',
            'res_model': 'mrp.bom.line',
            'domain': [('bom_id', '=', self.id)],
            'res_id': self.id,
        }

    def compute_count(self):
        for record in self:
            record.line_count = self.env['mrp.bom.line'].search_count([('bom_id', '=', self.id)])

    def _get_bom_total(self, lines):
        total = 0
        for line in lines:
            if line.child_bom_id:
                total += MrpBom._get_bom_total(self, line.child_bom_id.bom_line_ids)
            else:
                total += 1
        return total

    def _get_bom_total_recibido(self, lines):
        total_recibido = 0
        for line in lines:
            if line.child_bom_id:
                total_recibido += MrpBom._get_bom_total(self, line.child_bom_id.bom_line_ids)
            elif line.recibido:
                total_recibido += 1
        return total_recibido

    def _total_lineas(self):
        for record in self:
            record.total_lineas = MrpBom._get_bom_total(self, record.bom_line_ids)

    def _total_lineas_recibido(self):
        for record in self:
            record.total_lineas_recibido = MrpBom._get_bom_total_recibido(self, record.bom_line_ids)

    total_lineas = fields.Integer(string='Compras Total', required=False, compute=_total_lineas)
    total_lineas_recibido = fields.Integer(string='Compras Recibido', required=False, compute=_total_lineas_recibido)

    @api.onchange('trabajo')
    def onchange_trabajo(self):
        for rec in self:
            if rec.trabajo:
                rec.cliente = rec.trabajo.partner_id.id
                rec.analytic_account_id = rec.trabajo.analytic_account_id.id

    @staticmethod
    def recurse(lines, line_qty=1, count=0):
        for line in lines:
            count = count + 1
            all_components.append({'gestwin': line['n_pedido_compras'],
                                   'entregado': line['entregado'],
                                   'recibido': line['recibido'],
                                   'product_qty': line_qty * line.product_qty,
                                   'default_code': line['product_id']['default_code'],
                                   'name': line['product_id']['name'],
                                   'material': line['material'],
                                   'acabado': line['acabado'],
                                   'bom_count': line['product_id']['bom_count'],
                                   'level': count,
                                   'seccion': line['seccion']['name'],
                                   'subconjunto': line['subconjunto']['name'],
                                   'bom_id': line['bom_id']['id']
                                   })
            if len(line.child_line_ids) > 0:
                MrpBom.recurse(line.child_line_ids, line_qty=line_qty * line.product_qty)

    @staticmethod
    def compute_all_lines():
        components = []
        for component in all_components:
            components.append({'gestwin': component['gestwin'],
                               'entregado': component['entregado'],
                               'recibido': component['recibido'],
                               'product_qty': component['product_qty'],
                               'default_code': component['default_code'],
                               'name': component['name'],
                               'material': component['material'],
                               'acabado': component['acabado'],
                               'bom_count': component['bom_count'],
                               'level': component['level'],
                               'seccion': component['seccion'],
                               'subconjunto': component['subconjunto'],
                               'bom_id': component['bom_id']
                               })
        return components

    def compute_all_lines_and_sum(self):
        components = []
        key_list = []
        value_list = []
        all_components_sum = []
        secciones_name = []
        all_components_sum_by_section = []

        for component in all_components:
            unique_code = str(component['default_code']) + str(component['seccion'])
            components.append({'unique_code': unique_code,
                               'gestwin': component['gestwin'],
                               'entregado': component['entregado'],
                               'recibido': component['recibido'],
                               'product_qty': component['product_qty'],
                               'default_code': component['default_code'],
                               'name': component['name'],
                               'material': component['material'],
                               'acabado': component['acabado'],
                               'bom_count': component['bom_count'],
                               'level': component['level'],
                               'seccion': component['seccion'],
                               'subconjunto': component['subconjunto'],
                               'bom_id': component['bom_id']
                               })
        all_components.clear()
        all_components_sum.clear()
        all_components_sum_by_section.clear()
        for component in components:
            unique_code = str(component['default_code']) + str(component['seccion'])
            if unique_code not in [x['unique_code'] for x in all_components_sum]:
                all_components_sum.append({'unique_code': unique_code,
                                           'gestwin': component['gestwin'],
                                           'entregado': component['entregado'],
                                           'recibido': component['recibido'],
                                           'product_qty': component['product_qty'],
                                           'default_code': component['default_code'],
                                           'name': component['name'],
                                           'material': component['material'],
                                           'acabado': component['acabado'],
                                           'bom_count': component['bom_count'],
                                           # 'level': component['level'],
                                           'seccion': component['seccion'],
                                           'subconjunto': component['subconjunto'],
                                           'bom_id': component['bom_id']
                                           })
            else:
                for component_sum in all_components_sum:
                    if component_sum['unique_code'] == component['unique_code']:
                        component_sum['product_qty'] += component['product_qty']
        for rec in self.env['seccion'].search([]):
            secciones_name.append(rec.name)
        all_components_sum_by_section = sorted(all_components_sum, key=itemgetter('seccion'))
        for key, value in groupby(all_components_sum_by_section, key=itemgetter('seccion')):
            if key in secciones_name:
                key_list.append(key)
                value_list.append(list(value))

        for i in value_list:
            i.sort(key=lambda x: x['default_code'])

        return key_list, value_list

    def compute_all_lines_by_subconjunto(self):
        components = []
        key_list = []
        value_list = []
        secciones_name = []
        subconjuntos_name = []
        all_components_by_subconjunto = []

        for component in all_components:
            unique_code = str(component['default_code']) + str(component['seccion'])
            components.append({'unique_code': unique_code,
                               'gestwin': component['gestwin'],
                               'entregado': component['entregado'],
                               'recibido': component['recibido'],
                               'product_qty': component['product_qty'],
                               'default_code': component['default_code'],
                               'name': component['name'],
                               'material': component['material'],
                               'acabado': component['acabado'],
                               'bom_count': component['bom_count'],
                               'level': component['level'],
                               'seccion': component['seccion'],
                               'subconjunto': component['subconjunto'],
                               'bom_id': component['bom_id']
                               })
        all_components.clear()
        for rec in self.env['seccion'].search([]):
            secciones_name.append(rec.name)
        for rec2 in self.env['subconjunto'].search([]):
            subconjuntos_name.append(rec2.name)
        all_components_by_subconjunto = sorted(components, key=itemgetter('subconjunto', 'seccion'))
        for key, value in groupby(all_components_by_subconjunto, key=itemgetter('subconjunto', 'seccion')):
            if key[0] in subconjuntos_name:
                key_list.append(key[0] + ' - ' + key[1])
                value_list.append(list(value))

        for i in value_list:
            i.sort(key=lambda x: x['default_code'])

        return key_list, value_list
