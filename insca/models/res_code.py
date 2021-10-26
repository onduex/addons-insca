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
    product_route_ids = fields.Many2many(comodel_name="stock.location.route", string="Método abastecimiento",
                                         readonly=False, ondelete="cascade",
                                         domain=[('product_selectable', '=', True)])
    type_store = fields.Selection([
        ('consu', 'Consumible'),
        ('service', 'Servicio'),
        ('product', 'Almacenable')], string='Tipo de producto', default='product', required=False)
    date_schedule_mrp = fields.Float(string='Plazo fabricación', required=False, help="En días")
    date_schedule_customer = fields.Integer(string='Plazo cliente', required=False, help="En días")
    type_mrp = fields.Selection([
        ('normal', 'Fabricar'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontratación')], string='Tipo de LdM', default='normal', required=False)
    route_mrp = fields.Char(string='Ruta fija', required=False)
    categ_fixed = fields.Many2one(comodel_name='product.category', string='Categoría fija', required=False)
