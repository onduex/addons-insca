# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    vault_route = fields.Char(related='product_tmpl_id.vault_route', string='Vault Ruta', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bom in res:
            res_code = self.env['res.code'].search([('name', '=', bom.product_tmpl_id.vault_code)])
            if res_code.type_mrp:
                res.update({'type': res_code.type_mrp})
        return res
