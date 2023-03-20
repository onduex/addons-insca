# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('categ_id.parent_id.name') == 'MPRIMA' and \
                    vals.get('categ_id.category_base_id.name') == 'MADERA':
                vals['default_code'] = self.env['ir.sequence'].next_by_code('product.tab')
        return super(ProductTemplate, self).create(vals_list)