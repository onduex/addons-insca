# -*- coding: utf-8 -*-
# © 2023 Tomás Pascual (<tompascual@outlook.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def _get_active_id(self):
        return self._context.get('active_id')
