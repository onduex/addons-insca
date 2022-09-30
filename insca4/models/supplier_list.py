# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from datetime import date

po_line_id_metal_list = []


def dynamic_selection():
    today = str(date.today().strftime("%d/%m/%Y"))
    select = [('1', 'SI'),
              ('2', ('Pintecas ' + today)),
              ('3', ('Agricer ' + today)),
              ('4', ('Otros ' + today))]
    return select


def dynamic_selection2():
    today = str(date.today().strftime("%d/%m/%Y"))
    select = [('1', 'SI'),
              ('2', ('Insca ' + today)),
              ('3', ('Impeva ' + today)),
              ('4', ('Pintecas ' + today)),
              ('5', ('Otros ' + today))]
    return select


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "id asc"

    # Definir jerarquía
    category_id = fields.Many2one('library.book.category')
    sale_order = fields.Many2one(comodel_name='sale.order', string='Venta ref. ', required=False, readonly=True)
    purchase_order = fields.Many2one(comodel_name='purchase.order', string='Compra ref.', required=False, readonly=True)
    mrp_production = fields.Many2one(comodel_name='mrp.production', string='Fabricación ref.', required=False,
                                     readonly=True)
    product_template = fields.Many2one(comodel_name='product.template', string='Código + Nombre', required=False,
                                       readonly=True)
    vault_web_link = fields.Char(string='Web', required=False, readonly=True)
    commitment_date = fields.Datetime(string='Fecha prevista', required=False, readonly=True)
    partner_name = fields.Char(string='Cliente', required=False, readonly=True)
    product_origin = fields.Char(string='Producto origen', required=False, readonly=True)
    purchase_partner = fields.Char(string='Proveedor', required=False, readonly=True)
    product_code = fields.Char(string='Código', required=False, readonly=True)
    product_color = fields.Char(string='Color', required=False, readonly=True)
    product_material = fields.Char(string='Material', required=False, readonly=True)
    material_code = fields.Char(string='CM', required=False, readonly=True)
    color_code = fields.Char(string='CC', required=False, readonly=True)
    product_name = fields.Char(string='Nombre', required=False, readonly=True)
    product_quantity = fields.Float(string='Cantidad', required=False, readonly=True, store=True)
    product_uom_name = fields.Char(string='UoM', required=False, readonly=True)
    model_id = fields.Integer(string='Id del Modelo', required=False, readonly=True)
    type = fields.Char(string='Tipo', required=False, readonly=True)
    type_model_id = fields.Char(string='Ref. Interna', required=False, readonly=True)
    checked = fields.Boolean(string='Procesada', required=False)
    is_finished_line = fields.Boolean(string='Fabricado', compute='compute_is_finished_line', store=True)
    lmat = fields.Integer(string='LdM ID', required=False, readonly=True)
    lmat_level = fields.Integer(string='LdM Nivel', required=False, readonly=True)
    n0 = fields.Char(string='Nivel 0', required=False, readonly=True)
    n1 = fields.Char(string='Nivel 1', required=False, readonly=True)
    n2 = fields.Char(string='Nivel 2', required=False, readonly=True)
    n3 = fields.Char(string='Nivel 3', required=False, readonly=True)
    n4 = fields.Char(string='Nivel 4', required=False, readonly=True)
    n5 = fields.Char(string='Nivel 5', required=False, readonly=True)

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
    sal = fields.Selection(string='99-SAL',
                           selection=lambda self: dynamic_selection2(), required=False, readonly=False)

    @api.depends('lst', 'lsc', 'plg', 'cmz', 'man', 'sol', 'pin', 'sal')
    def compute_is_finished_line(self):
        for rec in self:
            if rec.lst != '1' and rec.lsc != '1' and rec.plg != '1' and \
               rec.cmz != '1' and rec.man != '1' and rec.sol != '1' and rec.pin != '1' and rec.sal != '1':
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
            # orden_principal = 'OP/00547'  # Sólo testing
            orden_principal_obj = self.env['mrp.production'].search([('name', '=', orden_principal)])
            sm_ids = self.env['stock.move'].search([('name', '=', orden_principal),
                                                    ('created_purchase_line_id', '!=', False)])

            # Check si existe y Crear el producto principal
            supplier_list_check = self.env['supplier.list'].search([('mrp_production.name', '=', orden_principal)])
            if not len(supplier_list_check):
                self.create({'checked': False,
                             'partner_name': orden_principal_obj.sale_id.partner_id.name,
                             'commitment_date': orden_principal_obj.sale_id.commitment_date,
                             'sale_order': orden_principal_obj.sale_id.id,
                             'product_origin': '[' + str(orden_principal_obj.product_id.default_code) + ']' + ' ' +
                            str(orden_principal_obj.product_id.name),
                             'mrp_production': orden_principal_obj.id,
                             'purchase_order': '',
                             'purchase_partner': '',
                             'product_template': orden_principal_obj.product_tmpl_id.id,
                             'vault_web_link': orden_principal_obj.product_tmpl_id.vault_web_link,
                             'product_code': orden_principal_obj.product_tmpl_id.default_code,
                             'product_name': orden_principal_obj.product_id.name,
                             'product_quantity': orden_principal_obj.product_qty,
                             'product_uom_name': 'Uds',
                             'color_code': orden_principal_obj.product_id.vault_color,
                             'product_color': orden_principal_obj.product_id.product_color,
                             'material_code': '',
                             'product_material': '',
                             # 'model_id': sm['id'],
                             # 'type': 'SML',
                             # 'type_model_id': str(sm['id']) + '-' + '1000',
                             'lmat': orden_principal_obj.bom_id.id,
                             'lmat_level': '0001',
                             'n0': orden_principal_obj.product_id.default_code,
                             'n1': '',
                             'n2': '',
                             'n3': '',
                             'n4': '',
                             'n5': '',
                             'sal': '1',
                             })

            for sm in sm_ids:
                purchaseorder = sm.created_purchase_line_id.order_id.id
                purchasepartner = sm.created_purchase_line_id.order_id.partner_id.name
                if sm.product_id.default_code[0:3] in ('A30', 'A31') and \
                        sm['id'] not in self._get_supplier_list_ids_for_sm():

                    mo_id = self.env['mrp.production'].search([('name', '=', sm.origin)])
                    code = sm.product_id.default_code
                    bom_ids_max = self._get_bom(code)

                    if sm.product_id.vault_material:
                        materialcode = sm.product_id.vault_material
                        materialname = self.env['product.category.inventor'].search([
                            ('code', '=', materialcode)])[0].categ_material_id.name

                    else:
                        materialcode = 'NA'
                        materialname = 'NA'

                    for bom in bom_ids_max:
                        route_list += bom['vault_route'].split("-", -1)

                    lmatid = mo_id.bom_id.id
                    n1 = mo_id.product_id.default_code
                    n2 = sm.product_tmpl_id.default_code
                    colorcode = sm.product_id.vault_color
                    productcolor = sm.product_id.product_color

                    # Crear los productos en las líneas de compra con MO
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
                                 'product_code': '-- ' + sm.product_tmpl_id.default_code,
                                 'product_name': sm.product_id.name,
                                 'product_quantity': sm.product_qty,
                                 'product_uom_name': sm.product_uom.name,
                                 'color_code': colorcode,
                                 'product_color': productcolor,
                                 'material_code': materialcode,
                                 'product_material': materialname,
                                 'model_id': sm['id'],
                                 'type': 'SML',
                                 'type_model_id': str(sm['id']) + '-' + '1000',
                                 'lmat': lmatid,
                                 'lmat_level': '1000',
                                 'n0': '',
                                 'n1': n1,
                                 'n2': '',
                                 'n3': '',
                                 'n4': '',
                                 'n5': '',
                                 'lst': '1' if 'LST' in route_list else '',
                                 'lsc': '1' if 'LSC' in route_list else '',
                                 'plg': '1' if 'PLG' in route_list else '',
                                 'cmz': '1' if 'CMZ' in route_list else '',
                                 'man': '1' if 'MAN' in route_list else '',
                                 'sol': '1' if 'SOL' in route_list else '',
                                 'pin': '1' if 'PIN' in route_list else '',
                                 })
                    self.your_function2(materialname, materialcode, orden_principal, lmatid, n1, n2,
                                        colorcode, productcolor)
        res = 'Good Job'
        return res

    @api.model
    def your_function2(self, materialname, materialcode, orden_principal, lmatid, n1, n2, colorcode, productcolor):
        route_list = []
        route_list2 = []
        supplier_list_ids = self.env['supplier.list'].search([('checked', '=', False),
                                                              ('product_code', 'not ilike', 'A00.')])
        for record in supplier_list_ids:
            record.write({'checked': True})
            code = record.product_template.default_code
            bom_ids_max = self._get_bom(code)
            x = 0
            for bom_line in bom_ids_max.bom_line_ids:
                code = bom_line.product_id.default_code
                if code:
                    bom_ids_max2 = self._get_bom(code)
                    for bom in bom_ids_max2:
                        n3 = bom.product_tmpl_id.default_code
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
                                     'product_code': '---- ' + bom.product_tmpl_id.default_code,
                                     'product_name': bom.product_tmpl_id.name,
                                     'product_quantity': record.product_quantity * bom.product_qty,
                                     'product_uom_name': bom.product_uom_id.name,
                                     'color_code': colorcode,
                                     'product_color': productcolor,
                                     'material_code': materialcode,
                                     'product_material': materialname,
                                     'model_id': '',
                                     'type': '',
                                     'type_model_id': record.type_model_id[:-4] + '1' + str(x) + '00',
                                     'lmat': lmatid,
                                     'lmat_level': '1' + str(x) + '00',
                                     'n0': '',
                                     'n1': '',
                                     'n2': n2,
                                     'n3': '',
                                     'n4': '',
                                     'n5': '',
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
                        if len(bom_ids_max3):
                            for bom in bom_ids_max3:
                                n4 = bom.product_tmpl_id.default_code
                                if bom['vault_route']:
                                    route_list2 += bom['vault_route'].split("-", -1)
                                    materialcode = bom.product_tmpl_id.vault_material_code
                                    materialname = self.env['product.template'].search([
                                                     ('default_code', '=', bom.product_tmpl_id.vault_material_code)]).name
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
                                                 'product_quantity': record.product_quantity *
                                                bom_line2.bom_id.product_qty * bom.product_qty,
                                                 'product_uom_name': bom.product_uom_id.name,
                                                 'color_code': colorcode,
                                                 'product_color': productcolor,
                                                 'material_code': materialcode,
                                                 'product_material': materialname,
                                                 'model_id': '',
                                                 'type': '',
                                                 'type_model_id': record.type_model_id[:-4] + '1' + str(x) + str(y) + '0',
                                                 'lmat': lmatid,
                                                 'lmat_level': '1' + str(x) + str(y) + '0',
                                                 'n0': '',
                                                 'n1': '',
                                                 'n2': '',
                                                 'n3': n3,
                                                 'n4': '',
                                                 'n5': '',
                                                 'lst': '1' if 'LST' in route_list2 else '',
                                                 'lsc': '1' if 'LSC' in route_list2 else '',
                                                 'plg': '1' if 'PLG' in route_list2 else '',
                                                 'cmz': '1' if 'CMZ' in route_list2 else '',
                                                 'man': '1' if 'MAN' in route_list2 else '',
                                                 'sol': '1' if 'SOL' in route_list2 else '',
                                                 'pin': '1' if 'PIN' in route_list2 else '',
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
                                                 'product_quantity': record.product_quantity *
                                                bom_line3.bom_id.product_qty * bom_line2.bom_id.product_qty *
                                                bom_line3.product_qty,
                                                 'product_uom_name': bom_line3.product_uom_id.name,
                                                 'color_code': colorcode,
                                                 'product_color': productcolor,
                                                 'material_code': materialcode,
                                                 'product_material': materialname,
                                                 'model_id': '',
                                                 'type': '',
                                                 'type_model_id': record.type_model_id[:-4] + '1' + str(x) + str(y) + str(z),
                                                 'lmat': lmatid,
                                                 'lmat_level': '1' + str(x) + str(y) + str(z),
                                                 'n0': '',
                                                 'n1': '',
                                                 'n2': '',
                                                 'n3': '',
                                                 'n4': n4,
                                                 'n5': bom_line3.product_tmpl_id.default_code,
                                                 'sal': '1',
                                                 })
                        else:
                            y = 0
                            for bom_line22 in bom_ids_max2.bom_line_ids:
                                code = bom_line22.product_id.default_code
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
                                             'product_template': bom_line22.product_tmpl_id.id,
                                             'product_code': '------ ' + bom_line22.product_tmpl_id.default_code,
                                             'product_name': bom_line22.product_id.name,
                                             'product_quantity': record.product_quantity * bom_line22.bom_id.product_qty *
                                            bom_line2.bom_id.product_qty * bom_line22.product_qty,
                                             'product_uom_name': bom_line22.product_uom_id.name,
                                             'color_code': colorcode,
                                             'product_color': productcolor,
                                             'material_code': bom_line22.product_tmpl_id.default_code,
                                             'product_material': bom_line22.product_tmpl_id.name,
                                             'model_id': '',
                                             'type': '',
                                             'type_model_id': record.type_model_id[:-4] + '1' + str(x) + str(y) + '0',
                                             'lmat': lmatid,
                                             'lmat_level': '1' + str(x) + str(y) + '0',
                                             'n0': '',
                                             'n1': '',
                                             'n2': '',
                                             'n3': n3,
                                             'n4': bom_line22.product_tmpl_id.default_code,
                                             'n5': '',
                                             'sal': '1',
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
