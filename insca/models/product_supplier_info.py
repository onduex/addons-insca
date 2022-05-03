# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        res_code = self.env['res.code'].search([('name', '=', vals.get('vault_code'))])
        if res_code.supplier_id:
            vals.update({'seller_ids': [(0, 0, {'min_qty': 1.0,
                                                'price': 1.0,
                                                'delay': 1.0,
                                                'name': res_code.supplier_id.id,
                                                'product_id': self.product_variant_id.id,
                                                }
                                         )]})
        return super(ProductTemplate, self).write(vals)
