# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        supplier_lines = []
        res_code = self.env['res.code'].search([('name', '=', vals.get('vault_code'))])

        # escribir proveedores
        for product in self:
            if product.is_vault_product and not product.is_old_revision:
                if res_code.supplier_ids:
                    for rec in res_code.supplier_ids:
                        supplier_lines.append((0, 0, {'min_qty': 1.0,
                                                      'price': 1.0,
                                                      'delay': 1.0,
                                                      'name': rec.id,
                                                      'product_id': self.product_variant_id.id,
                                                      }
                                               ))
                    vals.update({'seller_ids': supplier_lines})
        return super(ProductTemplate, self).write(vals)
