# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends('vault_internal_id')
    def _set_png_link(self):
        for product in self:
            if (product.default_code and product.default_code[0:3] == 'A00') or product.is_vault_product:
                suffix = ''
                if len(str(product.vault_revision)) == 1:
                    suffix = "_R0" + product.vault_revision
                elif len(str(product.vault_revision)) == 2:
                    suffix = "_R" + product.vault_revision
                product.png_link = ("rundll32.exe C:/WINDOWS/system32/shimgvw.dll,ImageView_Fullscreen R:/DTECNIC/PLANOS/0_PNG/" + product.default_code[0:3] + "/" +
                                    product.default_code[0:7] + "/" +
                                    product.default_code + suffix + ".png")

    png_link = fields.Char(string='PNG', store=True, compute='_set_png_link', readonly=False)


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    png_link = fields.Char(string='PNG', store=False, related='product_tmpl_id.png_link')
    vault_web_link = fields.Char(string='PNG', store=False, related='product_tmpl_id.vault_web_link')


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    png_link = fields.Char(string='PNG', store=False, related='product_tmpl_id.png_link')
    vault_web_link = fields.Char(string='PNG', store=False, related='product_tmpl_id.vault_web_link')
