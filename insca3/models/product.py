# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_been_verified = fields.Boolean(string='PTG OK', required=False, default=False)
    ptg_link = fields.Char(string='PTG', required=False, store=True)

    def action_check_has_been_verified_boolean(self):
        unique_product_ids = []
        for record in self:
            if record not in unique_product_ids:
                unique_product_ids.append(record)
        for rec in unique_product_ids:
            rec.has_been_verified = not rec.has_been_verified
