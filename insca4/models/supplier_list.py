# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from datetime import date

po_line_id_metal_list = []


def dynamic_selection():
    today = str(date.today().strftime("%d/%m/%Y"))
    select = [('1', 'SI'), ('2', ('Pintecas ' + today)), ('3', ('Agricer ' + today)), ('4', ('Otros ' + today))]
    return select


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "type_model_id, id asc"

    sale_order = fields.Many2one(comodel_name='sale.order', string='Venta ref.', required=False, readonly=True)
    purchase_order = fields.Many2one(comodel_name='purchase.order', string='Compra ref.', required=False, readonly=True)
    mrp_production = fields.Many2one(comodel_name='mrp.production', string='Fabricación ref.', required=False,
                                     readonly=True)
    product_template = fields.Many2one(comodel_name='product.template', string='Código + Nombre', required=False,
                                       readonly=True)
    vault_web_link = fields.Char(string='Vault Link', required=False, readonly=True)
    commitment_date = fields.Datetime(string='Fecha prevista', required=False)
    partner_name = fields.Char(string='Cliente', required=False, readonly=True)
    product_origin = fields.Char(string='Producto origen', required=True, readonly=True)
    purchase_partner = fields.Char(string='Proveedor', required=False, readonly=True)
    product_code = fields.Char(string='Código', required=True, readonly=True)
    product_color = fields.Char(string='Color', required=False, readonly=True)
    product_material = fields.Char(string='Material', required=False, readonly=True)
    material_code = fields.Char(string='CM', required=False, readonly=True)
    color_code = fields.Char(string='CC', required=False, readonly=True)
    product_name = fields.Char(string='Nombre', required=True, readonly=True)
    product_quantity = fields.Float(string='Cantidad', required=False, readonly=True, store=True)
    product_uom_name = fields.Char(string='UoM', required=True, readonly=True)
    model_id = fields.Integer(string='Id del Modelo', required=True, readonly=True)
    type = fields.Char(string='Tipo', required=True, readonly=True)
    type_model_id = fields.Char(string='Ref. Interna', required=True, readonly=True)
    checked = fields.Boolean(string='Procesada', required=False)
    is_finished_line = fields.Boolean(string='Fabricado', compute='compute_is_finished_line', store=True)
    lst = fields.Selection(string='01-LST',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    lsc = fields.Selection(string='02-LSC',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    plg = fields.Selection(string='03-PLG',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    cmz = fields.Selection(string='04-CMZ',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    man = fields.Selection(string='05-MAN',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    sol = fields.Selection(string='06-SOL',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)
    pin = fields.Selection(string='07-PIN',
                           selection=lambda self: dynamic_selection(), required=False, readonly=False)

    @api.depends('lst', 'lsc', 'plg', 'cmz', 'man', 'sol', 'pin')
    def compute_is_finished_line(self):
        for rec in self:
            if rec.lst != '1' and rec.lsc != '1' and rec.plg != '1' and \
               rec.cmz != '1' and rec.man != '1' and rec.sol != '1' and rec.pin != '1':
                rec.is_finished_line = True
            else:
                rec.is_finished_line = False

    @api.model
    def your_function(self):
        route_list = []
        po_origin_list = []
        po_ids = self.env['purchase.order'].search([])

        for po in po_ids:
            if po['origin']:
                po_origin_list += po['origin'].split(", ", -1)
        po_origin_list = list(set(filter(lambda x: x[0:2] == 'OP', po_origin_list)))

        for orden_principal in po_origin_list:
            orden_principal = 'OP/00600'  # Sólo testing
            sm_ids = self.env['stock.move'].search([('name', '=', orden_principal),
                                                    ('created_purchase_line_id', '!=', False)])

            for sm in sm_ids:
                purchaseorder = sm.created_purchase_line_id.order_id.id
                purchasepartner = sm.created_purchase_line_id.order_id.partner_id.name
                if sm.product_id.default_code[0:3] in ('A30', 'A31') and \
                        sm['id'] not in self._get_supplier_list_ids_for_sm():

                    mo_id = self.env['mrp.production'].search([('name', '=', sm.origin)])
                    code = sm.product_id.default_code
                    bom_ids_max = self._get_bom(code)

                    if sm.product_id.vault_material_code:
                        materialname = self.env['product.template'].search([('default_code', '=',
                                                                             sm.product_id.vault_material_code)]).name
                        materialcode = sm.product_id.vault_material
                    else:
                        materialname = 'NA'
                        materialcode = 'NA'

                    for bom in bom_ids_max:
                        route_list += bom['vault_route'].split("-", -1)
                    self.create({'checked': False,
                                 'partner_name': mo_id.sale_id.partner_id.name,
                                 'commitment_date': mo_id.sale_id.commitment_date,
                                 'sale_order': mo_id.sale_id.id,
                                 'product_origin': '[' + mo_id.product_id.default_code + ']' + ' ' +
                                                   mo_id.product_id.name,
                                 'mrp_production': self.env['mrp.production'].search([('name', '=', sm.origin)]).id,
                                 'purchase_order': purchaseorder,
                                 'purchase_partner': purchasepartner,
                                 'product_template': sm.product_tmpl_id.id,
                                 'vault_web_link': sm.product_tmpl_id.vault_web_link,
                                 'product_code': sm.product_tmpl_id.default_code,
                                 'product_name': sm.product_id.name,
                                 'product_quantity': sm.product_qty,
                                 'product_uom_name': sm.product_uom.name,
                                 'color_code': sm.product_id.vault_color,
                                 'product_color': sm.product_id.product_color,
                                 'material_code': materialcode,
                                 'product_material': materialname,
                                 'model_id': sm['id'],
                                 'type': 'SML',
                                 'type_model_id': str(sm['id']) + '-' + '1000',
                                 'lst': '1' if 'LST' in route_list else '',
                                 'lsc': '1' if 'LSC' in route_list else '',
                                 'plg': '1' if 'PLG' in route_list else '',
                                 'cmz': '1' if 'CMZ' in route_list else '',
                                 'man': '1' if 'MAN' in route_list else '',
                                 'sol': '1' if 'SOL' in route_list else '',
                                 'pin': '1' if 'PIN' in route_list else '',
                                 })
                    self.your_function2(materialname, materialcode, orden_principal)
        res = 'Good Job'
        return res

    @api.model
    def your_function2(self, materialname, materialcode, orden_principal):
        route_list = []
        route_list2 = []
        supplier_list_ids = self.env['supplier.list'].search([('checked', '=', False)])
        for record in supplier_list_ids:
            if not record['checked']:
                record.write({'checked': True})
                code = record.product_template.default_code
                bom_ids_max = self._get_bom(code)
                x = 0
                for bom_line in bom_ids_max.bom_line_ids:
                    code = bom_line.product_id.default_code
                    bom_ids_max2 = self._get_bom(code)
                    for bom in bom_ids_max2:
                        route_list += bom['vault_route'].split("-", -1)
                        purchaseorder = self.env['purchase.order.line'].search([
                            ('product_template_id.default_code', '=', bom.product_tmpl_id.default_code),
                            ('order_id.origin', 'ilike', orden_principal)
                        ]).order_id,
                        x = x + 1
                        self.create({'checked': True,
                                     'partner_name': self.env['sale.order'].
                                    search([('name', '=', record.sale_order.name)]).partner_id.name,
                                     'commitment_date': self.env['sale.order'].
                                    search([('name', '=', record.sale_order.name)]).commitment_date,
                                     'sale_order': record.sale_order.id,
                                     'product_origin': record.product_origin,
                                     'mrp_production': record.mrp_production.id,
                                     'purchase_order': purchaseorder[0].id,
                                     'purchase_partner': purchaseorder[0].partner_id.name,
                                     'product_template': bom.product_tmpl_id.id,
                                     'vault_web_link': bom.product_tmpl_id.vault_web_link,
                                     'product_code': '-- ' + bom.product_tmpl_id.default_code,
                                     'product_name': bom.product_tmpl_id.name,
                                     'product_quantity': record.product_quantity * bom.product_qty,
                                     'product_uom_name': bom.product_uom_id.name,
                                     'material_code': materialcode,
                                     'product_material': materialname,
                                     'model_id': '',
                                     'type': '',
                                     'type_model_id': record.type_model_id[:-4] + '1' + str(x) + '00',
                                     'lst': '1' if 'LST' in route_list else '',
                                     'lsc': '1' if 'LSC' in route_list else '',
                                     'plg': '1' if 'PLG' in route_list else '',
                                     'cmz': '1' if 'CMZ' in route_list else '',
                                     'man': '1' if 'MAN' in route_list else '',
                                     'sol': '1' if 'SOL' in route_list else '',
                                     'pin': '1' if 'PIN' in route_list else '',
                                     })
                        route_list = []

                    y = 0
                    for bom_line2 in bom_ids_max2.bom_line_ids:
                        code = bom_line2.product_id.default_code
                        bom_ids_max3 = self._get_bom(code)
                        for bom in bom_ids_max3:
                            if bom['vault_route']:
                                route_list2 += bom['vault_route'].split("-", -1)
                                y = y + 1
                                self.create({'checked': True,
                                             'partner_name': self.env['sale.order'].
                                            search([('name', '=', record.sale_order.name)]).partner_id.name,
                                             'commitment_date': self.env['sale.order'].
                                            search([('name', '=', record.sale_order.name)]).commitment_date,
                                             'sale_order': record.sale_order.id,
                                             'product_origin': record.product_origin,
                                             'mrp_production': record.mrp_production.id,
                                             'purchase_order': purchaseorder[0].id,
                                             'purchase_partner': purchaseorder[0].partner_id.name,
                                             'product_template': bom.product_tmpl_id.id,
                                             'vault_web_link': bom.product_tmpl_id.vault_web_link,
                                             'product_code': '------ ' + bom.product_tmpl_id.default_code,
                                             'product_name': bom.product_tmpl_id.name,
                                             'product_quantity': record.product_quantity * bom_line2.bom_id.product_qty * bom.product_qty,
                                             'product_uom_name': bom.product_uom_id.name,
                                             'material_code': materialcode,
                                             'product_material': materialname,
                                             'model_id': '',
                                             'type': '',
                                             'type_model_id': record.type_model_id[:-4] + '1' + str(x) + str(y) + '0',
                                             'lst': '1' if 'LST' in route_list else '',
                                             'lsc': '1' if 'LSC' in route_list else '',
                                             'plg': '1' if 'PLG' in route_list else '',
                                             'cmz': '1' if 'CMZ' in route_list else '',
                                             'man': '1' if 'MAN' in route_list else '',
                                             'sol': '1' if 'SOL' in route_list else '',
                                             'pin': '1' if 'PIN' in route_list else '',
                                             })
                                route_list2 = []

                            z = 0
                            for bom_line3 in bom_ids_max3.bom_line_ids:
                                code = bom_line3.product_id.default_code
                                bom_ids_max4 = self._get_bom(code)
                                z = z + 1
                                self.create({'checked': True,
                                             'partner_name': self.env['sale.order'].
                                            search([('name', '=', record.sale_order.name)]).partner_id.name,
                                             'commitment_date': self.env['sale.order'].
                                            search([('name', '=', record.sale_order.name)]).commitment_date,
                                             'sale_order': record.sale_order.id,
                                             'product_origin': record.product_origin,
                                             'mrp_production': record.mrp_production.id,
                                             'purchase_order': purchaseorder[0].id,
                                             'purchase_partner': purchaseorder[0].partner_id.name,
                                             'product_template': bom_line3.product_tmpl_id.id,
                                             'product_code': '---------- ' + bom_line3.product_tmpl_id.default_code,
                                             'product_name': bom_line3.product_id.name,
                                             'product_quantity': record.product_quantity * bom_line3.bom_id.product_qty * bom_line2.bom_id.product_qty * bom_line3.product_qty,
                                             'product_uom_name': bom_line3.product_uom_id.name,
                                             'material_code': materialcode,
                                             'product_material': materialname,
                                             'model_id': '',
                                             'type': '',
                                             'type_model_id': record.type_model_id[:-4] + '1' + str(x) + str(y) + str(z),
                                             })
        res = 'Obtener BoM'
        return res

    def _get_bom(self, code):
        return self.env['mrp.bom'].search([('product_tmpl_id.default_code', '=', code)])

    def _get_supplier_list_ids_for_sm(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'SML':  # Stock Move Line
                list_ids.append(rec['model_id'])
        return list_ids
