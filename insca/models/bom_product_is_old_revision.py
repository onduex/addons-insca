# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        if vals.get('is_old_revision'):
            for record in self.bom_ids:
                record.sudo().write({'active': False,
                                     'is_old_revision': True})
            vals.update({'active': False})

        return super(ProductTemplate, self).write(vals)
