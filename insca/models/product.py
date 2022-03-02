# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_categ = fields.Char(string='Vault Categoría', required=False)  # Categoria
    vault_categ_terminado = fields.Char(string='Vault Cat. PTERMINADO', required=False)  # Categoria PTERMINADO
    vault_code = fields.Char(string='Vault Código', required=False)  # 3 primeros digitos
    vault_material_code = fields.Char(string='Vault Virtual Material', required=False)  # Codigo_Virtual_Material
    vault_route = fields.Char(string='Vault Ruta', required=False)  # Ruta de produccion
    vault_material = fields.Char(string='Vault Material', required=False)  # Codigo material
    vault_edge_code = fields.Char(string='Vault Edge Code', required=False)  # Codigo cantos

    vault_color = fields.Char(string='Vault Color', required=False)  # Codigo color
    vault_length = fields.Char(string='Vault Largo', required=False)  # Largo
    vault_width = fields.Char(string='Vault Ancho', required=False)  # Ancho
    vault_height = fields.Char(string='Vault Hondo', required=False)  # Hondo
    vault_thinkness = fields.Char(string='Vault Espesor', required=False)  # Espesor
    vault_diameter = fields.Char(string='Vault Diámetro', required=False)  # Diametro
    vault_mesh = fields.Char(string='Vault Malla', required=False)  # Malla

    def write(self, vals):
        if self.is_vault_product:
            res_code = self.env['res.code'].search([('name', '=', self.vault_code)])
            if res_code:
                # Cambio tipo de datos
                if self.default_code:
                    vals.update({'vault_code': str(self.default_code)[0:3]})
                if vals.get('vault_length'):
                    vals.update({'product_length': float(vals.get('vault_length'))})
                if vals.get('vault_width'):
                    vals.update({'product_width': float(vals.get('vault_width'))})
                if vals.get('vault_height'):
                    vals.update({'product_height': float(vals.get('vault_height'))})
                if vals.get('vault_thinkness'):
                    vals.update({'product_thickness': float(vals.get('vault_thinkness'))})

                # Escribe material code
                if self.vault_material_code:
                    vals.update({'vault_material_code': self.vault_material_code})

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
                # Código A00
                if vals['vault_code'] == 'A00':
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ_terminado'])])
                    if categ:
                        vals.update({'categ_id': categ.id})

                # Código A10
                elif vals['vault_code'] == 'A10':
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ'])])
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    if categ and categ.name != parent_categ:
                        categ = self.env['product.category'].sudo().create({'name': vals.get('vault_categ'),
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    # Crear lista de materiales
                    if vals.get('vault_material_code'):
                        product_id = self.env['product.product'].\
                            search([('default_code', '=', vals['vault_material_code'])])
                        self.env['mrp.bom'].sudo().create({'product_tmpl_id': self.id,
                                                           'code': self.vault_revision,
                                                           'product_qty': 1,
                                                           'type': 'normal',
                                                           'bom_line_ids': [(0, 0, {'product_id': product_id.id,
                                                                                    'product_qty': 1}),
                                                                            ]
                                                           })
                    vals.update({'categ_id': categ.id})

                # Código A30 CON COLOR
                elif vals['vault_code'] == 'A30' and vals['vault_color'] and vals['vault_categ']:
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ'] + ' ' + 'COLOR')])
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    if not categ:
                        categ = self.env['product.category'].sudo(). \
                            create({'name': vals['vault_categ'] + ' ' + 'COLOR',
                                    'parent_id': parent_categ.id,
                                    })
                    # Crear lista de materiales
                    # if vals.get('vault_material_code'):
                    #     product_id = self.env['product.product']. \
                    #         search([('default_code', '=', vals['vault_material_code'])])
                    #     self.env['mrp.bom'].sudo().create({'product_tmpl_id': self.id,
                    #                                        'code': self.vault_revision,
                    #                                        'product_qty': 1,
                    #                                        'type': 'normal',
                    #                                        'bom_line_ids': [(0, 0, {'product_id': product_id.id,
                    #                                                                 'product_qty': 1}),
                    #                                                         ]
                    #                                        })
                    vals.update({'categ_id': categ.id})

        return super(ProductTemplate, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if vals.get('default_code'):
            res.update({'vault_code': vals['default_code'][0:3]
                        })
        return res
