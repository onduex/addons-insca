# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from smb.SMBConnection import SMBConnection
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def open_dir(self):
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        product_tmpl_obj = self.env['product.template']
        for record in self:
            # product_tmpl = product_tmpl_obj.search([('default_code', '=', record.folder_name)])
            conn = SMBConnection(res_company_obj.smb_user, res_company_obj.smb_pass,
                                 res_company_obj.odoo_server_name, res_company_obj.filestore_server_name)
            conn.connect(res_company_obj.filestore_server_ip, res_company_obj.filestore_server_port)

            # try:
            #     if not len(product_tmpl):
            #         product_tmpl_obj.create({'name': record.description,
            #                                  'default_code': record.folder_name,
            #                                  'type': "service",
            #                                  'categ_id': self.env['product.category']
            #                                 .search([('name', '=', 'EXPEDIENTE')]).id,
            #                                  'sale_ok': False,
            #                                  'purchase_ok': False,
            #                                  })
            #     else:
            #         product_tmpl.write({'name': record.description})
            #
            #     conn.createDirectory(res_company_obj.filestore_server_shared_folder,
            #                          "/" + res_company_obj.filestore_server_shared_folder_level1 + "/" +
            #                          record.folder_name + " " + record.description)
            #
            #     self.creadas = True
            #     for subfolder in self.subfolder_ids:
            #         conn.createDirectory(res_company_obj.filestore_server_shared_folder,
            #                              "/" + res_company_obj.filestore_server_shared_folder_level1 + "/" +
            #                              record.folder_name + " " + record.description + "/" + subfolder.name)
            # except Exception:
            #     conn.close()
            #     raise ValidationError(_('La carpeta %s ya existe. Check'
            #                             % (record.folder_name + " " + record.description)))
            conn.close()
