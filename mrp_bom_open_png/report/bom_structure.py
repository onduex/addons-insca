# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _


class BomStructureReport(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    @api.model
    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        res = super(BomStructureReport, self)._get_bom_lines(
            bom, bom_quantity, product, line_id, level
        )
        line_ids = self.env["mrp.bom.line"].search([("bom_id", "=", bom.id)])
        for line in res[0]:
            line_id = line_ids.filtered(
                lambda l: l.png_link and l.id == line["line_id"]
            )
            line_id1 = line_ids.filtered(
                lambda l: l.vault_web_link and l.id == line["line_id"]
            )
            line["png_link"] = line_id.png_link or ""
            line["vault_web_link"] = line_id1.vault_web_link or ""
        return res
