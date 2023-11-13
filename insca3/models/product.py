# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from smb.SMBConnection import SMBConnection
from odoo.exceptions import ValidationError
import subprocess


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_been_verified = fields.Boolean(string='PTG OK', required=False, default=False)
    ptg_link = fields.Char(string='PTG', required=False, store=True)
