# -*- coding: utf-8 -*-
# © 2023 Tomás Pascual (<tompascual@outlook.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CreateProductWiz(models.TransientModel):
    _name = 'create.product.wiz'
    _description = 'Wizard para crear productos desde la categoría'

    product_ids = fields.One2many(comodel_name='product.template', inverse_name='name',
                                  string='Productos existentes', required=False, readonly=True)


class ProductCategory(models.Model):
    _inherit = "product.category"

    def create_product_wiz_action(self):
        product_ids = self.env["product.template"].search([("categ_id", "=", self.id)])
        context = {'default_categ_id': self.id,
                   'default_product_ids': product_ids.ids,
                   }
        return {
            'name': 'Crear producto',
            'type': 'ir.actions.act_window',
            'res_model': 'create.product.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
