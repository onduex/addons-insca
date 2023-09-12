# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bom in res:
            suffix = ''
            if len(bom.product_tmpl_id.vault_revision) == 1:
                suffix = "_R0" + bom.product_tmpl_id.vault_revision
            elif len(bom.product_tmpl_id.vault_revision) == 2:
                suffix = "_R" + bom.product_tmpl_id.vault_revision
            bom.png_link = ("R:/DTECNIC/PLANOS/0_PNG/" + bom.product_tmpl_id.default_code[0:3] + "/" +
                            bom.product_tmpl_id.default_code[0:7] + "/" +
                            bom.product_tmpl_id.default_code + suffix + ".png")
            return res

    def write(self, values):
        super(MrpBom, self).write(values)
        if values.get('product_tmpl_id'):
            suffix = ''
            if len(self.product_tmpl_id.vault_revision) == 1:
                suffix = "_R0" + self.product_tmpl_id.vault_revision
            elif len(self.product_tmpl_id.vault_revision) == 2:
                suffix = "_R" + self.product_tmpl_id.vault_revision
            values.update({'png_link': ("R:/DTECNIC/PLANOS/0_PNG/" + self.product_tmpl_id.default_code[0:3] + "/" +
                                        self.product_tmpl_id.default_code[0:7] + "/" +
                                        self.product_tmpl_id.default_code + suffix + ".png")
                           })
            return super(MrpBom, self).write(values)

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True)


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bomLine in res:
            suffix = ''
            if len(bomLine.bom_id.code) == 1:
                suffix = "_R0" + bomLine.bom_id.code
            elif len(bomLine.bom_id.code) == 2:
                suffix = "_R" + bomLine.bom_id.code
            bomLine.png_link = ("R:/DTECNIC/PLANOS/0_PNG/" + bomLine.product_id.default_code[0:3] + "/" +
                                bomLine.product_id.default_code[0:7] + "/" +
                                bomLine.product_id.default_code + suffix + ".png")
            return res

    def write(self, values):
        super(MrpBomLine, self).write(values)
        if values.get('product_id'):
            for bomLine in self:
                suffix = ''
                if len(bomLine.bom_id.code) == 1:
                    suffix = "_R0" + bomLine.bom_id.code
                elif len(bomLine.bom_id.code) == 2:
                    suffix = "_R" + bomLine.bom_id.code
                values.update({'png_link': ("R:/DTECNIC/PLANOS/0_PNG/" + bomLine.product_id.default_code[0:3] + "/" +
                                            bomLine.product_id.default_code[0:7] + "/" +
                                            bomLine.product_id.default_code + suffix + ".png")
                               })
                return super(MrpBomLine, self).write(values)

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True)
