# -*- coding: utf-8 -*-
# © 2019 Sergio Díaz (<sdimar@yahoo.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.rainbow.tools.tools import (
    convert_date,
    get_literal_by_records,
    SEARCH_OPERATORS,
    serialize_zeep_object_list,
    VAULT_SERVER_DATETIME_FORMAT,
)


class PreviewImportWiz(models.TransientModel):
    _name = 'preview.import.wiz'
    _description = 'Preview products to import'

    items_to_import = fields.Text(string="", required=False, readonly=True, compute='list_vault_products')

    def list_vault_products(self):
        self.ensure_one()
        string = ''
        item = 0
        VaultServer = self.env['vault.server'].search([])
        products = VaultServer._list_vault_products()
        for product in products:
            item = item + 1
            items_to_import = ("{} - {} - {} - {} \n".format(item, product['ItemNum'],
                                                             product['Detail'], product['RevNum']))
            string += items_to_import
        self.items_to_import = string
        context = {'default_vault_server_id': self.id,
                   'default_items_to_import': self.items_to_import
                   }
        return {
            'name': 'Preview products',
            'type': 'ir.actions.act_window',
            'res_model': 'preview.import.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}


class VaultServer(models.Model):
    _inherit = "vault.server"

    def preview_import_wiz_action(self):
        context = {'default_vault_server_id': self.id
                   }
        return {
            'name': 'Preview products',
            'type': 'ir.actions.act_window',
            'res_model': 'preview.import.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
