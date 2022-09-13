# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "id asc"

    manufacturing_origin = fields.Char(string='Fabricación origen', required=False, readonly=True)
    product_origin = fields.Char(string='Producto origen', required=True, readonly=True)
    sale_origin = fields.Char(string='Venta origen', required=True, readonly=True)
    sale_name = fields.Char(string='Pedido', required=False, readonly=True)
    product_code = fields.Char(string='Código de producto', required=True, readonly=True)
    product_name = fields.Char(string='Producto', required=True, readonly=True)
    product_quantity = fields.Float(string='Cantidad', required=False, readonly=True)
    model_id = fields.Integer(string='Id del Modelo', required=True, readonly=True)
    type = fields.Char(string='Tipo', required=True, readonly=True)
    type_model_id = fields.Char(string='Código', required=True, readonly=True)
    checked = fields.Boolean(string='Procesada', required=False)
    pin = fields.Selection(string='_PIN',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    sol = fields.Selection(string='_SOL',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    man = fields.Selection(string='_MAN',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    lst = fields.Selection(string='_LST',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    lsc = fields.Selection(string='_LSC',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    plg = fields.Selection(string='_PLG',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    sec = fields.Selection(string='_SEC',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    cmz = fields.Selection(string='_CMZ',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)
    emb = fields.Selection(string='_EMB',
                           selection=[('1', 'SI'), ('2', 'OK')], required=False, readonly=False)

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
            sm_ids = self.env['stock.move'].search([('name', '=', 'OP/00516')])  # orden_principal
            po_id = self.env['purchase.order'].search([('origin', 'ilike', 'OP/00516'),
                                                       ('sale_order_id', '!=', False)])  # orden_principal
            if len(po_id):
                saleName = po_id[0].name
            else:
                saleName = 'NA'

            for sm in sm_ids:
                if sm.product_id.default_code[0:3] in ('A30', 'A31') and \
                        sm['id'] not in self._get_supplier_list_ids_for_sm():
                    mo_id = self.env['mrp.production'].search([('name', '=', sm.origin)])
                    code = sm.product_id.default_code
                    bom_ids_max = self._get_bom(code)
                    for bom in bom_ids_max:
                        route_list += bom['vault_route'].split("-", -1)
                    self.create({'checked': False,
                                 'sale_origin': mo_id.origin,
                                 'product_origin': '[' + mo_id.product_id.default_code + ']' + ' ' +
                                                   mo_id.product_id.name,
                                 'manufacturing_origin': sm.origin,
                                 'sale_name': saleName,
                                 'product_code': sm.product_id.default_code,
                                 'product_name': sm.product_id.name,
                                 'product_quantity': sm.product_qty,
                                 'model_id': sm['id'],
                                 'type': 'SML',
                                 'type_model_id': 'SML' + ' ' + str(sm['id']),
                                 'pin': '1' if 'PIN' in route_list else '',
                                 'sol': '1' if 'SOL' in route_list else '',
                                 'man': '1' if 'MAN' in route_list else '',
                                 'lst': '1' if 'LST' in route_list else '',
                                 'lsc': '1' if 'LSC' in route_list else '',
                                 'plg': '1' if 'PLG' in route_list else '',
                                 'sec': '1' if 'SEC' in route_list else '',
                                 'cmz': '1' if 'CMZ' in route_list else '',
                                 'emb': '1' if 'EMB' in route_list else '',
                                 })
                    self.your_function2()
        res = 'Good Job'
        return res

    @api.model
    def your_function2(self):
        route_list = []
        route_list2 = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for record in supplier_list_ids:
            if not record['checked']:
                record.write({'checked': True})
                code = record.product_code
                bom_ids_max = self._get_bom(code)
                # for bom in bom_ids_max:
                #     print('N1', bom.product_tmpl_id.default_code, bom.vault_route)
                for bom_line in bom_ids_max.bom_line_ids:
                    code = bom_line.product_id.default_code
                    bom_ids_max2 = self._get_bom(code)
                    for bom in bom_ids_max2:
                        # print('  N2', bom.product_tmpl_id.default_code, bom.vault_route)
                        route_list += bom['vault_route'].split("-", -1)
                        self.create({'checked': True,
                                     'sale_origin': record.sale_origin,
                                     'product_origin': record.product_origin,
                                     'manufacturing_origin': record.manufacturing_origin,
                                     'sale_name': '',
                                     'product_code': '__ ' + bom.product_tmpl_id.default_code,
                                     'product_name': bom.product_tmpl_id.name,
                                     'product_quantity': record.product_quantity * bom.product_qty,
                                     'model_id': '',
                                     'type': '',
                                     'type_model_id': record.type_model_id,
                                     'pin': '1' if 'PIN' in route_list else '',
                                     'sol': '1' if 'SOL' in route_list else '',
                                     'man': '1' if 'MAN' in route_list else '',
                                     'lst': '1' if 'LST' in route_list else '',
                                     'lsc': '1' if 'LSC' in route_list else '',
                                     'plg': '1' if 'PLG' in route_list else '',
                                     'sec': '1' if 'SEC' in route_list else '',
                                     'cmz': '1' if 'CMZ' in route_list else '',
                                     'emb': '1' if 'EMB' in route_list else '',
                                     })
                        route_list = []

                    for bom_line2 in bom_ids_max2.bom_line_ids:
                        code = bom_line2.product_id.default_code
                        bom_ids_max3 = self._get_bom(code)
                        for bom in bom_ids_max3:
                            if bom['vault_route']:
                                # print('    N3', bom.product_tmpl_id.default_code, bom.vault_route)
                                route_list2 += bom['vault_route'].split("-", -1)
                                self.create({'checked': True,
                                             'sale_origin': record.sale_origin,
                                             'product_origin': record.product_origin,
                                             'manufacturing_origin': record.manufacturing_origin,
                                             'sale_name': '',
                                             'product_code': '____ ' + bom.product_tmpl_id.default_code,
                                             'product_name': bom.product_tmpl_id.name,
                                             'product_quantity': record.product_quantity * bom_line2.bom_id.product_qty * bom.product_qty,
                                             'model_id': '',
                                             'type': '',
                                             'type_model_id': record.type_model_id,
                                             'pin': '1' if 'PIN' in route_list2 else '',
                                             'sol': '1' if 'SOL' in route_list2 else '',
                                             'man': '1' if 'MAN' in route_list2 else '',
                                             'lst': '1' if 'LST' in route_list2 else '',
                                             'lsc': '1' if 'LSC' in route_list2 else '',
                                             'plg': '1' if 'PLG' in route_list2 else '',
                                             'sec': '1' if 'SEC' in route_list2 else '',
                                             'cmz': '1' if 'CMZ' in route_list2 else '',
                                             'emb': '1' if 'EMB' in route_list2 else '',
                                             })
                                route_list2 = []

                            for bom_line3 in bom_ids_max3.bom_line_ids:
                                code = bom_line3.product_id.default_code
                                bom_ids_max4 = self._get_bom(code)
                                # print('      N4', code)
                                self.create({'checked': True,
                                             'sale_origin': record.sale_origin,
                                             'product_origin': record.product_origin,
                                             'manufacturing_origin': record.manufacturing_origin,
                                             'sale_name': '',
                                             'product_code': '______ ' + bom_line3.product_id.default_code,
                                             'product_name': bom_line3.product_id.name,
                                             'product_quantity': record.product_quantity * bom_line3.bom_id.product_qty * bom_line2.bom_id.product_qty * bom_line3.product_qty,
                                             'model_id': '',
                                             'type': '',
                                             'type_model_id': record.type_model_id,
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
