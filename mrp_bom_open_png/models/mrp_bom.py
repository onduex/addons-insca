# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bom in res:
            bom.png_link = ("C:/IMG/0_PNG/" + bom.product_tmpl_id.default_code[0:3] + "/" +
                            bom.product_tmpl_id.default_code[0:7] + "/" +
                            bom.product_tmpl_id.default_code + ".png")
            return res

    def write(self, values):
        super(MrpBom, self).write(values)
        if values.get('product_tmpl_id'):
            values.update({'png_link': ("C:/IMG/0_PNG/" + self.product_tmpl_id.default_code[0:3] + "/" +
                                        self.product_tmpl_id.default_code[0:7] + "/" +
                                        self.product_tmpl_id.default_code + ".png")
                           })
            return super(MrpBom, self).write(values)

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True)


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for bomLine in res:
            bomLine.png_link = ("C:/IMG/0_PNG/" + bomLine.product_id.default_code[0:3] + "/" +
                                bomLine.product_id.default_code[0:7] + "/" +
                                bomLine.product_id.default_code + ".png")
            return res

    def write(self, values):
        super(MrpBomLine, self).write(values)
        if values.get('product_id'):
            values.update({'png_link': ("C:/IMG/0_PNG/" + self.product_id.default_code[0:3] + "/" +
                                        self.product_id.default_code[0:7] + "/" +
                                        self.product_id.default_code + ".png")
                           })
            return super(MrpBomLine, self).write(values)

    png_link = fields.Char(string='PNG', required=False, readonly=False, store=True)
