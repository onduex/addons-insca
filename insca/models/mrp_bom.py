# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    vault_route = fields.Char(related='product_tmpl_id.vault_route', string='Vault Ruta', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bom in res:
            res_code = self.env['res.code'].search([('name', '=', bom.product_tmpl_id.vault_code)])
            mrp_routing = self.env['mrp.routing'].search([('name', '=', bom.product_tmpl_id.vault_route)])

            if mrp_routing:
                res.update({'routing_id': mrp_routing.id})
            if res_code.type_mrp:
                res.update({'type': res_code.type_mrp})
        return res

    # def write(self, values):
    #     res = super().write(values)
    #     for bom in self:
    #         print(bom)
    #     return res
