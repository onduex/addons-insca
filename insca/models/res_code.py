# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResCode(models.Model):
    _name = "res.code"
    _description = "Objeto para la correcta creación/actualización de las propiedades de los productos"

    name = fields.Char(string='Código', required=False)
    app = fields.Char(string='Aplicación', required=False)
    type = fields.Char(string='Tipo', required=False)
    sale_ok = fields.Boolean(string='Puede ser vendido', required=False)
    purchase_ok = fields.Boolean(string='Puede ser comprado', required=False)
    product_route_ids = fields.Many2many(comodel_name="stock.location.route", string="Rutas", readonly=False,
                                         ondelete="cascade", domain=[('product_selectable', '=', True)])
    type_store = fields.Selection([
        ('consu', 'Consumible'),
        ('service', 'Servicio'),
        ('product', 'Almacenable')], string='Tipo de producto', default='product', required=False)
    date_schedule_mrp = fields.Integer(string='Plazo fabricación', required=False, help="En días")
    date_schedule_customer = fields.Integer(string='Plazo cliente', required=False, help="En días")
    type_mrp = fields.Selection([
        ('normal', 'Fabricar'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontratación')], string='Tipo de LdM', default='normal', required=False)
    route_mrp = fields.Char(string='Ruta fabricación', required=False)


    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplate, self).create(vals)
    #     res.update({'vault_code': vals['default_code'][0:3]
    #                 })
    #     return res
    #
    # def write(self, vals):
    #     if self.default_code:
    #         vals.update({'vault_code': str(self.default_code)[0:3]})
    #     if self.vault_length:
    #         vals.update({'product_length': float(self.vault_length)})
    #     if self.vault_width:
    #         vals.update({'product_width': float(self.vault_width)})
    #     if self.vault_height:
    #         vals.update({'product_height': float(self.vault_height)})
    #     if self.vault_thinkness:
    #         vals.update({'product_thickness': float(self.vault_thinkness)})
    #     res = super(ProductTemplate, self).write(vals)
    #     return res
