# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_categ = fields.Char(string='Vault Categoría', required=False)                     # Categoria
    vault_categ_terminado = fields.Char(string='Vault Cat. PTERMINADO', required=False)     # Categoria PTERMINADO
    vault_code = fields.Char(string='Vault Código', required=False)                         # 3 primeros digitos
    vault_material_code = fields.Char(string='Vault Virtual Material', required=False)      # Codigo_Virtual_Material
    vault_route = fields.Char(string='Vault Ruta', required=False)                          # Ruta de produccion
    vault_material = fields.Char(string='Vault Material', required=False)                   # Codigo material
    vault_edge_code = fields.Char(string='Vault Cod. Cantos', required=False)               # Codigo cantos
    vault_edge_num = fields.Char(string='Vault Num. Cantos', required=False)                # Número cantos
    vault_edge_len = fields.Char(string='Vault Long. Cantos', required=False)               # Longitud cantos
    vault_length_sheet = fields.Char(string='Vault Largo Chapa', required=False)            # Largo Chapa
    vault_width_sheet = fields.Char(string='Vault Ancho Chapa', required=False)             # Ancho Chapa

    vault_color = fields.Char(string='Vault Color', required=False)                         # Codigo color
    vault_sup_pintada = fields.Char(string='Vault Sup. Pintada', required=False)            # Superficie pintada
    vault_sup_madera = fields.Char(string='Vault Sup. Madera', required=False)              # Superficie madera
    vault_weight = fields.Char(string='Vault Peso', required=False)                         # Peso
    vault_length = fields.Char(string='Vault Largo', required=False)                        # Largo
    vault_width = fields.Char(string='Vault Ancho', required=False)                         # Ancho
    vault_height = fields.Char(string='Vault Hondo', required=False)                        # Hondo
    vault_thinkness = fields.Char(string='Vault Espesor', required=False)                   # Espesor
    vault_diameter = fields.Char(string='Vault Diámetro', required=False)                   # Diametro
    vault_mesh = fields.Char(string='Vault Malla', required=False)                          # Malla
    vault_program_assoc = fields.Boolean(string='Vault P. Asociado', required=False)        # CNC

    def write(self, vals):
        mrp_bom_object = self.env['mrp.bom']
        if self.is_vault_product and not self.is_old_revision:
            res_code = self.env['res.code'].search([('name', '=', self.vault_code)])
            if res_code:
                # Cambio tipo de datos
                if self.vault_code:
                    vals.update({'vault_code': self.vault_code})
                if vals.get('vault_length'):
                    vals.update({'product_length': float(vals.get('vault_length'))})
                if vals.get('vault_width'):
                    vals.update({'product_width': float(vals.get('vault_width'))})
                if vals.get('vault_height'):
                    vals.update({'product_height': float(vals.get('vault_height'))})
                if vals.get('vault_thinkness'):
                    vals.update({'product_thickness': float(vals.get('vault_thinkness'))})
                if vals.get('vault_diameter'):
                    vals.update({'vault_diameter': float(vals.get('vault_diameter'))})
                if vals.get('vault_mesh'):
                    vals.update({'vault_mesh': float(vals.get('vault_mesh'))})

                # Recupera valores
                if not vals.get('vault_categ'):
                    vals.update({'vault_categ': self.categ_id.name})
                if not vals.get('vault_color'):
                    vals.update({'vault_color': self.vault_color})
                if not vals.get('vault_route'):
                    vals.update({'vault_route': self.vault_route})
                if not vals.get('vault_edge_code'):
                    vals.update({'vault_edge_code': self.vault_edge_code})
                if not vals.get('vault_categ_terminado') and vals['vault_code'] == 'A00':
                    vals.update({'vault_categ_terminado': self.categ_id.name})

                # Escribe material code
                if not vals.get('vault_material_code'):
                    vals.update({'vault_material_code': self.vault_material_code})

                if vals.get('vault_internal_id'):
                    # si rainbow modifica el vault_internal_id se actualizara
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
                    if categ and vals['vault_categ_terminado'] != vals['vault_categ']:
                        vals.update({'categ_id': categ.id})
                    if not categ:
                        raise ValidationError(_('La categoría (%s) no está en Odoo' % vals['vault_categ_terminado']))

                # Código A10
                elif vals['vault_code'] == 'A10':
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                 ('parent_id', '=', parent_categ.id)
                                                                 ])
                    if not categ:
                        categ = self.env['product.category'].sudo().create({'name': vals.get('vault_categ'),
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    vals.update({'categ_id': categ.id})

                    # Check si existe ruta
                    mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                    if vals['vault_route'] and not len(mrp_routing):
                        raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                % (vals['vault_route'], vals['name'])))
                    # Crear lista de materiales
                    if len(self.bom_ids) == 0:
                        if vals.get('vault_material_code') or vals['vault_edge_code'] or vals['vault_color']:
                            lines = []
                            product_ids = []
                            if vals['vault_material_code']:
                                product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                  vals['vault_material_code'])])
                            if vals['vault_edge_code']:
                                product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                    vals['vault_edge_code'])])
                            if vals['vault_color']:
                                product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                    vals['vault_color'])])
                            for product in product_ids:
                                lines.append((0, 0, {'product_id': product.id, 'product_qty': 1}))
                            mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                               'code': self.vault_revision,
                                                               'product_qty': 1,
                                                               'type': 'normal',
                                                               'routing_id': mrp_routing.id or None,
                                                               'bom_line_ids': lines,
                                                          })

                # Código A30
                elif vals['vault_code'] == 'A30' and vals['vault_categ']:
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                 ('parent_id', '=', parent_categ.id)])
                    if not categ:
                        categ = self.env['product.category'].sudo().create({'name': vals['vault_categ'],
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    vals.update({'categ_id': categ.id})

                    # Check si existe ruta
                    mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                    if vals['vault_route'] and not len(mrp_routing):
                        raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                % (vals['vault_route'], vals['name'])))

                    # Check si existe producto sin pintar
                    product_zero = self.env['product.product'].search([('default_code', '=',
                                                                       self.default_code[:-3] + '000')])
                    if not len(product_zero):
                        raise ValidationError(_('Producto %s no encontrado. Revise Vault'
                                                % (self.default_code[:-3] + '000')))

                    # Crear lista de materiales
                    if len(self.bom_ids) == 0 and self.default_code[-3:] == '000':
                        if vals.get('vault_material_code'):
                            lines = []
                            product_ids = []
                            if vals['vault_material_code']:
                                product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                   vals['vault_material_code'])])
                            for product in product_ids:
                                lines.append((0, 0, {'product_id': product.id, 'product_qty': 1}))
                            mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                               'code': self.vault_revision,
                                                               'product_qty': 1,
                                                               'type': 'normal',
                                                               'routing_id': mrp_routing.id or None,
                                                               'bom_line_ids': lines,
                                                          })

                # Código A30P
                elif vals['vault_code'] == 'A30P' and vals['vault_categ']:
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                 ('parent_id', '=', parent_categ.id)])
                    if not categ:
                        categ = self.env['product.category'].sudo().create({'name': vals['vault_categ'],
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    vals.update({'categ_id': categ.id})

                    # Check si existe ruta
                    mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                    if vals['vault_route'] and not len(mrp_routing):
                        raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                % (vals['vault_route'], vals['name'])))

                    # Check si existe producto sin pintar
                    product_zero = self.env['product.product'].search([('default_code', '=',
                                                                        self.default_code[:-3] + '000')])
                    if not len(product_zero):
                        raise ValidationError(_('Producto %s no encontrado. Revise Vault'
                                                % (self.default_code[:-3] + '000')))

                    # Crear lista de materiales
                    if len(self.bom_ids) == 0 and self.default_code[-3:] != '000':
                        if vals['vault_color']:
                            lines = []
                            product_ids = []
                            product_ids_max = self.env['product.product'].search([('default_code', '=',
                                                                                   self.default_code[:-3] + '000')])
                            if vals['vault_color']:
                                product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                    vals['vault_color'])])
                            product_ids += max(product_ids_max)
                            for product in product_ids:
                                lines.append((0, 0, {'product_id': product.id, 'product_qty': 1}))
                            mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                          'product_id': self.product_variant_id.id,
                                                          'code': self.vault_revision,
                                                          'product_qty': 1,
                                                          'type': 'normal',
                                                          'routing_id': mrp_routing.id or None,
                                                          'bom_line_ids': lines,
                                                          })

                # Código A31
                elif vals['vault_code'] == 'A31' and vals['vault_categ']:
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                 ('parent_id', '=', parent_categ.id)])
                    if not categ:
                        categ = self.env['product.category'].sudo().create({'name': vals['vault_categ'],
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    vals.update({'categ_id': categ.id})

                    # Check si existe ruta
                    mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                    if vals['vault_route'] and not len(mrp_routing):
                        raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                % (vals['vault_route'], vals['name'])))

                    # Check si existe producto sin pintar
                    product_zero = self.env['product.product'].search([('default_code', '=',
                                                                        self.default_code[:-3] + '000')])
                    if not len(product_zero):
                        raise ValidationError(_('Producto %s no encontrado. Revise Vault'
                                                % (self.default_code[:-3] + '000')))

                # Código A31P
                elif vals['vault_code'] == 'A31P' and vals['vault_categ']:
                    parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                    categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                 ('parent_id', '=', parent_categ.id)])
                    if not categ:
                        categ = self.env['product.category'].sudo().create({'name': vals['vault_categ'],
                                                                            'parent_id': parent_categ.id,
                                                                            })
                    vals.update({'categ_id': categ.id})

                    # Check si existe ruta
                    mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                    if vals['vault_route'] and not len(mrp_routing):
                        raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                % (vals['vault_route'], vals['name'])))

                    # Check si existe producto sin pintar
                    product_zero = self.env['product.product'].search([('default_code', '=',
                                                                        self.default_code[:-3] + '000')])
                    if not len(product_zero):
                        raise ValidationError(_('Producto %s no encontrado. Revise Vault'
                                                % (self.default_code[:-3] + '000')))

                # Para valores predeterminados
                if res_code.route_mrp:
                    vals.update({'vault_route': res_code.route_mrp})
                if res_code.categ_fixed:
                    vals.update({'categ_id': res_code.categ_fixed.id})
                if res_code.uom_dimensions:
                    vals.update({'dimensional_uom_id': res_code.uom_dimensions.id})

        return super(ProductTemplate, self).write(vals)

    @api.model
    def create(self, vals):
        var = ''
        res = super(ProductTemplate, self).create(vals)

        if res.is_vault_product:
            if vals.get('default_code')[0:3] == 'A30' and vals.get('default_code')[-3:] != '000':
                var = vals['default_code'][0:3] + 'P'
            elif vals.get('default_code')[0:3] == 'A31' and vals.get('default_code')[-3:] != '000':
                var = vals['default_code'][0:3] + 'P'
            elif vals.get('default_code'):
                var = vals['default_code'][0:3]

            # estas funcionan porque no las importa rainbow
            res_code = self.env['res.code'].search([('name', '=', var)])
            res.update({'sale_ok': res_code.sale_ok,
                        'purchase_ok': res_code.purchase_ok,
                        'produce_delay': res_code.date_schedule_mrp,
                        'route_ids': [(6, 0, [x.id for x in res_code.product_route_ids])],
                        'type': res_code.type_store,
                        })
            res.update({'vault_code': var})

        return res
