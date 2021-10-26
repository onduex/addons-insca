# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_length = fields.Char(string='Vault Largo', required=False)
    vault_width = fields.Char(string='Vault Ancho', required=False)
    vault_height = fields.Char(string='Vault Hondo', required=False)
    vault_thinkness = fields.Char(string='Vault Espesor', required=False)
    vault_route = fields.Char(string='Vault Ruta', required=False)
    vault_code = fields.Char(string='Vault Código', required=False)
    vault_material = fields.Char(string='Vault Material', required=False)
    vault_color = fields.Char(string='Vault Color', required=False)
    vault_categ = fields.Char(string='Vault Categoría', required=False)

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if vals.get('default_code'):
            res.update({'vault_code': vals['default_code'][0:3]
                        })
        return res

    def write(self, vals):
        if self.is_vault_product:
            res_code = self.env['res.code'].search([('name', '=', self.vault_code)])
            if res_code:

                # Cambio tipo de datos
                if self.default_code:
                    vals.update({'vault_code': str(self.default_code)[0:3]})
                if self.vault_length:
                    vals.update({'product_length': float(self.vault_length)})
                if self.vault_width:
                    vals.update({'product_width': float(self.vault_width)})
                if self.vault_height:
                    vals.update({'product_height': float(self.vault_height)})
                if self.vault_thinkness:
                    vals.update({'product_thickness': float(self.vault_thinkness)})

                # Para valores predeterminados
                if res_code.route_mrp:
                    vals.update({'vault_route': res_code.route_mrp})
                if res_code.categ_fixed:
                    vals.update({'categ_id': res_code.categ_fixed})

                vals.update({'sale_ok': res_code.sale_ok,
                             'purchase_ok': res_code.purchase_ok,
                             'produce_delay': res_code.date_schedule_mrp,
                             'route_ids': [(6, 0, [x.id for x in res_code.product_route_ids])],
                             'type': res_code.type_store,
                             })

                # Para categorías dinámicas
                if not res_code.categ_fixed and vals['vault_code'] == 'A00':
                    categ = self.env['product.category'].search([('name', '=', self.vault_categ)])
                    parent_categ = res_code.type
                    print(categ, parent_categ)

        res = super(ProductTemplate, self).write(vals)
        return res
