# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.depends('product_tmpl_id', 'product_id', 'product_tmpl_id.vault_internal_id')
    def _set_png_link(self):
        for bom in self:
            if bom.product_tmpl_id.default_code[0:3] == 'A00' or bom.product_tmpl_id.is_vault_product:
                suffix = ''
                if len(str(bom.product_tmpl_id.vault_revision)) == 1:
                    suffix = "_R0" + bom.product_tmpl_id.vault_revision
                elif len(str(bom.product_tmpl_id.vault_revision)) == 2:
                    suffix = "_R" + bom.product_tmpl_id.vault_revision
                bom.png_link = ("R:/DTECNIC/PLANOS/0_PNG/" + bom.product_tmpl_id.default_code[0:3] + "/" +
                                bom.product_tmpl_id.default_code[0:7] + "/" +
                                bom.product_tmpl_id.default_code + suffix + ".png")

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True, compute='_set_png_link')


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.depends('product_id', 'product_tmpl_id.vault_revision', 'product_tmpl_id.vault_internal_id')
    def _set_png_link(self):
        for bomLine in self:
            if bomLine.product_tmpl_id.default_code[0:3] == 'A00' or bomLine.product_tmpl_id.is_vault_product:
                suffix = ''
                if len(str(bomLine.product_tmpl_id.vault_revision)) == 1:
                    suffix = "_R0" + bomLine.product_tmpl_id.vault_revision
                elif len(str(bomLine.product_tmpl_id.vault_revision)) == 2:
                    suffix = "_R" + bomLine.product_tmpl_id.vault_revision
                bomLine.png_link = ("R:/DTECNIC/PLANOS/0_PNG/" + bomLine.product_tmpl_id.default_code[0:3] + "/" +
                                    bomLine.product_tmpl_id.default_code[0:7] + "/" +
                                    bomLine.product_tmpl_id.default_code + suffix + ".png")

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True, compute='_set_png_link')
