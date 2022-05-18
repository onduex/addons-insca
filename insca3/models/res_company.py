# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    smb_user = fields.Char(string='SMB User', required=False)
    smb_pass = fields.Char(string='SMB Pass', required=False)
    odoo_server_name = fields.Char(string='Odoo Srv Name', required=False)
    filestore_server_name = fields.Char(string='Filestore Srv Name', required=False)
    filestore_server_ip = fields.Char(string='Filestore Srv IP', required=False)
    filestore_server_port = fields.Char(string='Filestore Srv Port', required=False)
    filestore_server_shared_folder = fields.Char(string='Filestore Srv Shared Folder', required=False)
    filestore_server_shared_folder_level1 = fields.Char(string='Filestore Srv Shared Folder L1', required=False)
    ds_sequence_start = fields.Integer(string='Inicio Sec. DS', required=False)
