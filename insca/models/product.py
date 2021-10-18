# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_length = fields.Char(string='Vault Longitud', required=False)
    vault_height = fields.Char(string='Vault Alto', required=False)
    vault_thinkness = fields.Char(string='Vault Espesor', required=False)
    vault_route = fields.Char(string='Vault Ruta', required=False)
    vault_code = fields.Char(string='Vault Código', required=False)
    vault_material = fields.Char(string='Vault Material', required=False)
    vault_color = fields.Char(string='Vault Color', required=False)
    vault_categ = fields.Char(string='Vault Categoría', required=False)
