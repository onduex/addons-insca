# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_material = fields.Char(string='Vault Material', required=False)
    vault_weight = fields.Char(string='Vault Weight', required=False)
    vault_color = fields.Char(string='Vault Color', required=False)
