# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rb_length = fields.Char(string='Longitud', required=False)
    rb_height = fields.Char(string='Alto', required=False)
    rb_thinkness = fields.Char(string='Espesor', required=False)
    rb_route = fields.Char(string='Ruta', required=False)
    rb_code = fields.Char(string='Código', required=False)
    rb_material = fields.Char(string='Material', required=False)
    rb_color = fields.Char(string='Color', required=False)
    rb_categ = fields.Char(string='Categoría', required=False)
