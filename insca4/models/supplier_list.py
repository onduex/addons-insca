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
    model_id = fields.Integer(string='Id del Modelo', required=True, readonly=True)
    type = fields.Char(string='Tipo', required=True, readonly=True)
    type_model_id = fields.Char(string='Código', required=True, readonly=True)

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

    @api.model
    def your_function(self):
        so_line_ids = self.env['sale.order.line'].search([])

        # only for sale order lines
        # line['product_id']['default_code'][0:9] == 'A00.03321' and
        for so_line in so_line_ids:
            if so_line['product_id']['default_code'] and so_line['order_id']['state'] == 'sale' and \
                    so_line['id'] not in self._get_supplier_list_ids_for_so():
                mo_id = self.env['mrp.production'].search([('origin', '=', so_line['order_id']['name'])])
                self.create({'sale_origin': so_line['order_id']['name'],
                             'product_origin': so_line['product_id']['default_code'],
                             'manufacturing_origin': mo_id['main_production_id']['name'],
                             'sale_name': so_line['order_id']['name'],
                             'product_code': so_line['product_id']['default_code'],
                             'product_name': so_line['product_id']['name'],
                             'model_id': so_line['id'],
                             'type': 'SOL',
                             'type_model_id': 'SOL' + str(so_line['id']),
                             })

        # searching po_line for each sale order
        supplier_list_ids = self.env['supplier.list'].search([('type', '=', 'SOL')])
        for each in supplier_list_ids:
            po_line_ids = self.env['purchase.order.line'].search([('order_id.origin', 'ilike', each['sale_name'])])

            for po_line in po_line_ids:
                if po_line['product_id']['default_code'] and \
                        po_line['id'] not in self._get_supplier_list_ids_for_po():
                    self.create({'sale_origin': each['sale_name'],
                                 'product_origin': each['product_code'],
                                 'manufacturing_origin': each['manufacturing_origin'],
                                 'sale_name': po_line['order_id']['name'],
                                 'product_code': po_line['product_id']['default_code'],
                                 'product_name': po_line['product_id']['name'],
                                 'model_id': po_line['id'],
                                 'type': 'POL',
                                 'type_model_id': 'POL' + str(po_line['id']),
                                 })

        res = 'Good Job'
        return res
