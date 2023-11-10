# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from smb.SMBConnection import SMBConnection
from odoo.exceptions import ValidationError
import subprocess


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    has_folder = fields.Boolean(string='Carpeta', required=False, store=True,
                                related='product_id.has_folder')
    has_been_verified = fields.Boolean(string='PTG OK', required=False, default=False,
                                       related='product_id.has_been_verified')
    ptg_link = fields.Char(string='PTG', required=False, store=True,
                           related='product_id.ptg_link')

    def action_check_has_been_verified_boolean(self):
        for record in self:
            record.product_id.has_been_verified = not record.product_id.has_been_verified

    @api.model
    def check_dir(self):
        folders = []
        a10_searched = ''
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        product_tmpl_ids = self.env['product.template'].search(['|', ('default_code', 'ilike', 'A10.'),
                                                                ('default_code', 'ilike', 'A11.')])

        for record in product_tmpl_ids:
            print(record.default_code)

        conn = SMBConnection(res_company_obj.smb_user,
                             res_company_obj.smb_pass,
                             res_company_obj.odoo_server_name,
                             res_company_obj.filestore_server_name
                             )
        conn.connect(res_company_obj.filestore_server_ip,
                     res_company_obj.filestore_server_port
                     )
        results = conn.listPath(res_company_obj.filestore_server_shared_folder_2,
                                '/' + res_company_obj.filestore_server_shared_folder_level1_2,
                                timeout=30)
        for rec in results:
            folders.append(rec.filename)

        for record in product_tmpl_ids:
            if record.default_code[4] == '0':
                a10_searched = record.default_code[0:4] + record.default_code[5:-7]
            elif record.default_code[4] == '1':
                a10_searched = 'B' + record.default_code[1:4] + record.default_code[5:-7]

            if a10_searched in folders:
                record.has_folder = True
                record.ptg_link = ("H:/" + res_company_obj.filestore_server_shared_folder_level1_2
                                   + "/" + a10_searched)
            else:
                record.has_folder = False
                record.ptg_link = ""

        conn.close()
