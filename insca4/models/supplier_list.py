# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class Supplierlist(models.Model):
    _name = 'supplier.list'
    _description = "Lista para proveedores de las piezas/ensamblajes requeridos de los pedidos activos"
    _order = "sale_name desc"

    sale_name = fields.Char(string='Pedido', required=True, readonly=True)
    product_code = fields.Char(string='Código', required=True, readonly=True)
    product_name = fields.Char(string='Producto', required=True, readonly=True)

    @api.model
    def your_function(self):
        so_line_ids = self.env['sale.order.line'].search([])
        for line in so_line_ids:
            if line['product_id']['default_code'] and line['product_id']['default_code'][0:9] == 'A00.03321':
                self.create({'sale_name': line['order_id']['name'],
                             'product_code': line['product_id']['default_code'],
                             'product_name': line['product_id']['name'],
                             })

        res = 'Finalmente ha salido, madre mía'
        return res
