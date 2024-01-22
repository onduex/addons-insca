# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    vault_material_name = fields.Char(string='Nombre virtual', required=False,
                                      related='product_id.vault_material_name',
                                      store=True)
    png_link = fields.Char(string='PNG', store=False, related='product_id.png_link')
    png_a00_link = fields.Char(string='A00', store=False, related='main_production_id.product_id.png_link')
    vault_web_link = fields.Char(string='VLT', store=False, related='product_id.vault_web_link')
