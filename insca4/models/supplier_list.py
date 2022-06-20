# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "sale_name desc"

    sale_name = fields.Char(string='Pedido', required=True, readonly=True)
    product_code = fields.Char(string='Código de producto', required=True, readonly=True)
    product_name = fields.Char(string='Producto', required=True, readonly=True)
    model_id = fields.Integer(string='Id del Modelo', required=True, readonly=True)
    type = fields.Char(string='Tipo', required=True, readonly=True)
    type_model_id = fields.Char(string='Código', required=True, readonly=True)

    def _get_supplier_list_ids_for_sales(self):
        list_ids = []
        supplier_list_ids = self.env['supplier.list'].search([])
        for rec in supplier_list_ids:
            if rec['type'] == 'SOL':
                list_ids.append(rec['model_id'])
        return list_ids

    @api.model
    def your_function(self):
        so_line_ids = self.env['sale.order.line'].search([])

        # only for sale order lines
        for line in so_line_ids:
            if line['product_id']['default_code'] and \
                    line['product_id']['default_code'][0:9] == 'A00.03321' and \
                    line['id'] not in self._get_supplier_list_ids_for_sales():
                self.create({'sale_name': line['order_id']['name'],
                             'product_code': line['product_id']['default_code'],
                             'product_name': line['product_id']['name'],
                             'model_id': line['id'],
                             'type': 'SOL',
                             'type_model_id': 'SOL' + str(line['id']),
                             })

        res = 'Finalmente ha salido, madre mía'
        return res
