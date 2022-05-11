# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os
from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _
from smb.SMBConnection import SMBConnection
from odoo.exceptions import ValidationError


class ResFolder(models.Model):
    _name = "res.folder"
    _description = "Modelo para almacenar la estructura de carpetas a crear"

    name = fields.Char(string='Código', required=False, store=True, readonly=True)
    folder_name = fields.Char(string='Nombre', required=False, store=True, readonly=True)
    description = fields.Char(string='Descripción', required=True, store=True)
    creadas = fields.Boolean(string='Creadas', required=False, default=False)
    subfolder_ids = fields.Many2many(comodel_name='res.subfolder', string='SubCarpetas', required=False)

    @api.model
    def create(self, vals):
        res = super(ResFolder, self).create(vals)
        used_keywords = []
        codigo_ids = self.env['res.folder'].search([])
        numbers = list(range(0, 100000))
        numbers_list = [str(item).zfill(6) for item in numbers]
        res_subfolder_ids = self.env['res.subfolder'].search([])

        for record in codigo_ids[:-1]:
            used_keywords.append(record.name)

        difference = list(set(numbers_list).difference(used_keywords))
        difference.sort(reverse=False)
        res.update({'name': difference[0],
                    'folder_name': 'DS' + difference[0],
                    'subfolder_ids': [(6, 0, [x.id for x in res_subfolder_ids])],
                    })
        return res

    def make_dir(self):
        res_company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        for record in self:
            conn = SMBConnection(res_company_obj.smb_user, res_company_obj.smb_pass,
                                 res_company_obj.odoo_server_name, res_company_obj.filestore_server_name)
            conn.connect(res_company_obj.filestore_server_ip, res_company_obj.filestore_server_port)

            try:
                conn.createDirectory(res_company_obj.filestore_server_shared_folder,
                                     "/" + res_company_obj.filestore_server_shared_folder_level1 + "/" +
                                     record.folder_name + " " + record.description)
                self.creadas = True
                for subfolder in self.subfolder_ids:
                    conn.createDirectory(res_company_obj.filestore_server_shared_folder,
                                         "/" + res_company_obj.filestore_server_shared_folder_level1 + "/" +
                                         record.folder_name + " " + record.description + "/" + subfolder.name)
            except Exception:
                raise ValidationError(_('La carpeta %s ya existe. Check'
                                        % (record.folder_name + " " + record.description)))
            conn.close()
