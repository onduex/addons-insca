# -*- coding: utf-8 -*-
# © 2019 Sergio Díaz (<sdimar@yahoo.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreatePackagingWiz(models.TransientModel):
    _name = 'create.packaging.wiz'
    _description = 'Wizard para crear LdM de embalajes'

    product_id = fields.Many2one(
        comodel_name='product.template', string="Producto",
        help="Producto a embalar", ondelete='cascade', readonly=True)
    embalaje_id = fields.Many2one(
        comodel_name='product.template', string="Embalaje",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    embalaje_bom = fields.Many2one(
        comodel_name='mrp.bom', string="LdM",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    n_bulto_lines = fields.Integer(string='Nº de bulto', required=False, compute='onchange_values')
    largo = fields.Integer(string='Largo', required=False)
    ancho = fields.Integer(string='Ancho', required=False)
    alto = fields.Integer(string='Alto', required=False)
    espesor_general = fields.Selection(string='Espesor general', selection=[('16', '16'), ('19', '19'), ],
                                       required=False, )
    espesor_base = fields.Selection(string='Espesor base', selection=[('25', '25'), ('30', '30'), ], required=False, )
    n_tacos = fields.Integer(string='Nº de tacos', required=False, default=4)
    n_bultos = fields.Integer(string='Nº de bultos', required=False, default=1)

    bulto = fields.Char(string='Bulto', required=False, readonly=True)
    tapa = fields.Char(string='Tapa', required=False, readonly=True)
    base = fields.Char(string='Base', required=False, readonly=True)
    l_largo = fields.Char(string='Lateral largo', required=False, readonly=True)
    l_corto = fields.Char(string='Lateral corto', required=False, readonly=True)
    taco = fields.Char(string='Taco', required=False, readonly=True)

    tapa_id = fields.Integer(string='Tapa Id', required=False, readonly=True)
    base_id = fields.Integer(string='Base Id', required=False, readonly=True)
    l_largo_id = fields.Integer(string='Lateral largo Id', required=False, readonly=True)
    l_corto_id = fields.Integer(string='Lateral corto Id', required=False, readonly=True)
    taco_id = fields.Integer(string='Taco Id', required=False, readonly=True)

    @api.onchange('largo', 'ancho', 'alto', 'espesor_base', 'espesor_general', 'n_tacos', 'n_bultos')
    def onchange_values(self):
        self.n_bulto_lines = len(self.embalaje_bom.bom_line_ids)

        self.bulto = 'BULTO ' + str(self.largo) + 'X' + str(self.ancho) + 'X' + \
                     str(self.alto) + 'mm'
        self.tapa = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.ancho) + 'X' + \
                    str(self.espesor_general) + 'mm'
        self.base = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.ancho) + 'X' + \
                    str(self.espesor_base) + 'mm'
        self.l_largo = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.alto) + 'X' + \
                       str(self.espesor_general) + 'mm'
        self.l_corto = 'PIEZA EMBALAJE ' + str(self.alto) + 'X' + str(self.ancho) + 'X' + \
                       str(self.espesor_general) + 'mm'
        self.taco = 'TACO ' + '80X80mm'

        self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
        self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)])

    def create_bom(self):
        self.onchange_values()
        product_ids = []
        product_tmpl_obj = self.env['product.template']
        mrp_bom_obj = self.env['mrp.bom']
        if self.largo == 0 or \
                self.ancho == 0 or \
                self.alto == 0 or \
                self.espesor_base == 0 or \
                self.n_tacos == 0:
            raise ValidationError(_('¡Obligatorio todas las dimensiones distintas de cero!'))

        # Crear primer nivel de embalaje
        if len(self.embalaje_bom.bom_line_ids) < 10:
            default_code = 'B0' + str(len(self.embalaje_bom.bom_line_ids) + 1) + '.' + self.embalaje_id.default_code[4:]
        else:
            default_code = 'B' + str(len(self.embalaje_bom.bom_line_ids) + 1) + '.' + self.embalaje_id.default_code[4:]
        bulto_id = self.env["product.template"].search([("default_code", "=", default_code)])
        if bulto_id:
            raise ValidationError(
                _('El bulto %s ya existe' % bulto_id['default_code']))
        # Crear nuevo bulto
        new_id = product_tmpl_obj.create({'name': self.bulto,
                                          'default_code': default_code,
                                          'type': "product",
                                          'categ_id': self.embalaje_id.categ_id.id,
                                          'sale_ok': False,
                                          'purchase_ok': False,
                                          })['id']
        product_obj = self.env['product.product'].search([('product_tmpl_id', '=', new_id)])
        # Crear LdM del bulto
        new_bom_id = mrp_bom_obj.sudo().create({'product_tmpl_id': new_id,
                                                'product_id': product_obj.id,
                                                'product_qty': 1,
                                                'type': 'normal',
                                                'routing_id': 44,  # SEC-EMB
                                                })
        # Crear bulto como línea de LdM
        self.env['mrp.bom.line'].sudo().create({'bom_id': self.embalaje_bom.id,
                                                'product_id': product_obj.id,
                                                'product_qty': self.n_bultos})
        self.n_bultos = 1
        self.largo = 0
        self.ancho = 0
        self.alto = 0

        # Tapa
        self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
        if self.tapa_id:
            product_ids.append({'id': self.tapa_id,
                                'qty': 1,
                                })
        if not self.tapa_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.tapa,
                                                               'default_code': 'EM01.' + self.embalaje_id.default_code[
                                                                                         4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'vault_material_code': 'VT.00AAM0'
                                                                                      + str(
                                                                   self.espesor_general) + 'mm',
                                                               'vault_length': str(self.largo),
                                                               'vault_width': str(self.ancho),
                                                               'vault_thinkness': str(self.espesor_general),
                                                               }).id,
                                'qty': 1,
                                })

        # Base
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        if self.base_id:
            product_ids.append({'id': self.base_id,
                                'qty': 1,
                                })
        if not self.base_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.base,
                                                               'default_code': 'EM02.' + self.embalaje_id.default_code[
                                                                                         4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'vault_material_code': 'VT.00AAM0'
                                                                                      + str(self.espesor_base) + 'mm',
                                                               'vault_length': str(self.largo),
                                                               'vault_width': str(self.ancho),
                                                               'vault_thinkness': str(self.espesor_base),
                                                               }).id,
                                'qty': 1,
                                })

        # Lateral largo
        self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
        if self.l_largo_id:
            product_ids.append({'id': self.l_largo_id,
                                'qty': 2,
                                })
        if not self.l_largo_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.l_largo,
                                                               'default_code': 'EM03.' + self.embalaje_id.default_code[
                                                                                         4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'vault_material_code': 'VT.00AAM0'
                                                                                      + str(
                                                                   self.espesor_general) + 'mm',
                                                               'vault_length': str(self.largo),
                                                               'vault_width': str(self.alto),
                                                               'vault_thinkness': str(self.espesor_general),
                                                               }).id,
                                'qty': 2,
                                })

        # Lateral corto
        self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
        if self.l_corto_id:
            product_ids.append({'id': self.l_corto_id,
                                'qty': 2,
                                })
        if not self.l_corto_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.l_corto,
                                                               'default_code': 'EM04.' + self.embalaje_id.default_code[
                                                                                         4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'vault_material_code': 'VT.00AAM0'
                                                                                      + str(
                                                                   self.espesor_general) + 'mm',
                                                               'vault_length': str(self.alto),
                                                               'vault_width': str(self.ancho),
                                                               'vault_thinkness': str(self.espesor_general),
                                                               }).id,
                                'qty': 2,
                                })

        # Taco
        taco_material = self.env["res.packaging"].search([("name", "=", 'Material tacos')])
        self.taco_id = self.env["product.template"].search([("default_code", "=", taco_material.code)])
        if self.taco_id:
            product_ids.append({'id': self.taco_id,
                                'qty': self.n_tacos,
                                })
        if not self.taco_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.taco,
                                                               'default_code': 'EM05.' + self.embalaje_id.default_code[
                                                                                         4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': self.n_tacos,
                                })

        # Crear las líneas de la LdM del bulto
        for rec in product_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec['id'])]).id
            exist = self.env['mrp.bom.line'].search([('bom_id', '=', new_bom_id.id),
                                                     ('product_id', '=', product_id)])

            if not exist:
                self.env['mrp.bom.line'].sudo().create({'bom_id': new_bom_id.id,
                                                        'product_id': product_id,
                                                        'product_qty': rec['qty']})
            else:
                exist.update({'product_qty': exist['product_qty'] + rec['qty']})

        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.packaging.wiz',
            'context': self.env.context,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new'}


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def create_bom_wiz_action(self):
        embalaje_id = self.env["product.template"].search([("default_code", "ilike",
                                                            'EM0.' + self.default_code[4:10])])
        embalaje_bom = self.env["mrp.bom"].search([("product_tmpl_id", "=", embalaje_id.id)])

        if not embalaje_bom:
            raise ValidationError(
                _('El embalaje %s no tiene LdM' % embalaje_id['default_code']))

        context = {'default_product_id': self.id,
                   'default_embalaje_id': embalaje_id.id,
                   'default_embalaje_bom': max(embalaje_bom).id or None,
                   }
        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.packaging.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
