# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "sale_name desc"

    manufacturing_origin = fields.Char(string='Fabricación origen', required=False, readonly=True)
    product_origin = fields.Char(string='Producto origen', required=True, readonly=True)
    sale_origin = fields.Char(string='Venta origen', required=True, readonly=True)
    sale_name = fields.Char(string='Pedido', required=True, readonly=True)
    product_code = fields.Char(string='Código de producto', required=True, readonly=True)
    product_name = fields.Char(string='Producto', required=True, readonly=True)
    product_quantity = fields.Float(string='Cantidad', required=False)
    model_id = fields.Integer(string='Id del Modelo', required=True, readonly=True)
    type = fields.Char(string='Tipo', required=True, readonly=True)
    type_model_id = fields.Char(string='Código', required=True, readonly=True)

    @api.model
    def your_function(self):
        po_origin_list = []
        po_ids = self.env['purchase.order'].search([])
        mo_ids = self.env['mrp.production'].search([])

        for po in po_ids:
            po_origin_list += po['origin'].split(", ", -1)
        po_origin_list = list(set(filter(lambda x: x[0:2] == 'OP', po_origin_list)))
        # print(po_origin_list)

        for orden_principal in po_origin_list:
            sm_ids = self.env['stock.move'].search([('name', '=', orden_principal)])
            po_id = self.env['purchase.order'].search([('origin', 'ilike', orden_principal),
                                                       ('sale_order_id', '!=', False)])
            # print(po_id.name)
            for sm in sm_ids:
                if sm.product_id.default_code[0:3] in ('A30', 'A31') and \
                        sm['id'] not in self._get_supplier_list_ids_for_sm():
                    mo_id = self.env['mrp.production'].search([('name', '=', sm.origin)])
                    self.create({'sale_origin': mo_id.origin,
                                 'product_origin': '[' + mo_id.product_id.default_code + ']' + ' ' +
                                                   mo_id.product_id.name,
                                 'manufacturing_origin': sm.origin,
                                 'sale_name': po_id.name,
                                 'product_code': sm.product_id.default_code,
                                 'product_name': sm.product_id.name,
                                 'product_quantity': sm.product_qty,
                                 'model_id': sm['id'],
                                 'type': 'SML',
                                 'type_model_id': 'SML' + ' ' + str(sm['id']),
                                 })
        res = 'Good Job'
        return res

    @api.model
    def your_function2(self):
        po_origin_list = []
        po_ids = self.env['purchase.order'].search([('sale_order_id', '=', False)])
        for po in po_ids:
            po_origin_list += po['origin'].split(", ", -1)
        po_origin_list = list(set(filter(lambda x: x[0:2] == 'WH', po_origin_list)))
        # print(po_origin_list)
        for picking in po_origin_list:
            sm_ids = self.env['stock.picking'].search([('name', '=', picking)])
            po_id = self.env['purchase.order'].search([('origin', 'ilike', op), ('sale_order_id', '!=', False)])
            # print(po_id.name)
            for sm in sm_ids:
                if sm.product_id.default_code[0:3] in ('A30', 'A31') and \
                        sm['id'] not in self._get_supplier_list_ids_for_sm():
                    mo_id = self.env['mrp.production'].search([('name', '=', sm.origin)])

        res = 'Good Job 2'
        return res

    def _get_supplier_list_ids_for_sm(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'SML':  # Stock Move Line
                list_ids.append(rec['model_id'])
        return list_ids

    def _get_supplier_list_ids_for_so(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'SOL':  # Sale Order Line
                list_ids.append(rec['model_id'])
        return list_ids

    def _get_supplier_list_ids_for_po(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'POL':  # Purchase Order Line
                list_ids.append(rec['model_id'])
        return list_ids

    def _get_supplier_list_ids_for_mo(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'MO_':  # Manufacturing Order
                list_ids.append(rec['model_id'])
        return list_ids


