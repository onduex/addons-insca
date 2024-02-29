# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vault_state = fields.Char(string='ESTADO', required=False)
    vault_code = fields.Char(string='CODIGO TRUNCADO', required=False)
    vault_categ_terminado = fields.Char(string='00 CAT. PTERMINADO', required=False)  # Texto
    # 01 NOTAS INTERNAS --> description                                               # Texto
    vault_program_assoc = fields.Boolean(string='02 P. ASOCIADO', required=False)  # Booleano
    vault_width = fields.Char(string='ANCHO', required=False)  # Texto
    vault_width_sheet = fields.Char(string='ANCHO CHAPA', required=False)  # Texto
    vault_width_cut = fields.Char(string='ANCHO CORTE', required=False)  # Texto
    vault_working_face = fields.Boolean(string='CARA BUENA', required=False)  # Booleano
    vault_categ = fields.Char(string='CATEGORIA', required=False)  # Texto
    vault_edge_code = fields.Char(string='CODIGO CANTOS', required=False)  # Texto
    vault_color = fields.Char(string='CODIGO COLOR', required=False)  # Texto
    vault_edge_pin_code = fields.Char(string='COD COLOR CANTOS', required=False)  # Texto
    vault_edge_pin_name = fields.Char(string='COLOR CANTOS', required=False)  # Texto
    vault_material = fields.Char(string='CODIGO MATERIAL', required=False)  # Texto
    vault_material_code = fields.Char(string='CODIGO VIRTUAL', required=False)  # Texto
    vault_material_name = fields.Char(string='NOMBRE VIRTUAL', required=False)  # Texto
    # COLOR MATERIAL --> product_color                                          # Texto
    vault_purchase_code = fields.Char(string='CODIGO COMPRA', required=False)  # Texto
    vault_left_hand = fields.Char(string='CODIGO IZQ', required=False)  # Texto
    vault_right_hand = fields.Char(string='CODIGO DER', required=False)  # Texto
    vault_diameter = fields.Char(string='DIAMETRO', required=False)  # Texto
    vault_thinkness = fields.Char(string='ESPESOR', required=False)  # Texto
    vault_height = fields.Char(string='HONDO', required=False)  # Texto
    vault_length = fields.Char(string='LARGO', required=False)  # Texto
    vault_length_sheet = fields.Char(string='LARGO CHAPA', required=False)  # Texto
    vault_length_cut = fields.Char(string='LARGO CORTE', required=False)  # Texto
    vault_length_tub = fields.Char(string='LARGO TUBO', required=False)  # Texto
    vault_edge_len = fields.Char(string='L CANTOS CHAPADOS', required=False)  # Texto
    vault_mesh = fields.Char(string='MALLA', required=False)  # Texto
    vault_edge_num = fields.Char(string='NRO CANTOS CHAPADOS', required=False)  # Texto
    vault_edge_num_pin = fields.Char(string='NRO CANTOS PINTADOS', required=False)  # Texto
    vault_painted_face = fields.Integer(string='NRO CARAS PINTADAS', required=False)  # Integer
    vault_weight = fields.Char(string='PESO', required=False)  # Texto
    vault_edge_paint = fields.Char(string='PINTAR CANTOS', required=False)  # Texto
    vault_route = fields.Char(string='RUTA PRODUCCION', required=False)  # Texto
    vault_edge_painted_sup = fields.Char(string='SUP. CANTOS PINTADOS', required=False)  # Texto
    vault_sup_madera = fields.Char(string='SUP. PIEZA', required=False)  # Texto
    vault_sup_pintada = fields.Float(string='SUP. PINTURA', required=False)  # Float

    def write(self, vals):
        if self.env.context.get('bypass_vault'):
            return super(ProductTemplate, self).write(vals)
        mrp_bom_object = self.env['mrp.bom']
        for record in self:

            # Código A00
            if str(record.default_code)[0:3] == 'A00' and 'categ_id' in vals and vals['categ_id'] == 2584:
                vals.update({'categ_id': record.categ_id.id,
                             'type': 'product',
                             })
            elif str(record.default_code)[0:3] == 'A00' and 'categ_id' not in vals:
                vals.update({'categ_id': record.categ_id.id,
                             'type': 'product',
                             })

            if record.is_vault_product and not record.is_old_revision:
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
                        vals.update({'vault_categ_terminado': record.vault_categ_terminado})
                    if not vals.get('vault_purchase_code'):
                        vals.update({'vault_purchase_code': self.vault_purchase_code})
                    if not vals.get('vault_left_hand'):
                        vals.update({'vault_left_hand': self.vault_left_hand})
                    if not vals.get('vault_right_hand'):
                        vals.update({'vault_right_hand': self.vault_right_hand})
                    if not vals.get('vault_length_cut'):
                        vals.update({'vault_length_cut': self.vault_length_cut})
                    if not vals.get('vault_sup_madera'):
                        vals.update({'vault_sup_madera': self.vault_sup_madera})
                    if not vals.get('vault_sup_pintada'):
                        vals.update({'vault_sup_pintada': self.vault_sup_pintada})
                    if not vals.get('default_code'):
                        vals.update({'default_code': self.default_code})
                    if not vals.get('vault_material_name'):
                        vals.update({'vault_material_name': self.vault_material_name})
                    if not vals.get('product_color'):
                        vals.update({'product_color': self.product_color})
                    if not vals.get('vault_edge_pin_code'):
                        vals.update({'vault_edge_pin_code': self.vault_edge_pin_code})

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
                    # Código EM0
                    if vals['vault_code'] == 'EM0':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', res_code.route_mrp)])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))
                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:
                            mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                          'code': self.vault_revision,
                                                          'product_qty': 1,
                                                          'type': 'normal',
                                                          'routing_id': mrp_routing.id or None,
                                                          })

                    # Código A60S
                    if vals['vault_code'] == 'A60S':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', res_code.route_mrp)])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))
                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:
                            lines = []
                            product_ids = []
                            product_ids = self.env['product.product'].search([('default_code', '=', 'MP.000129')])
                            for product in product_ids:
                                if vals.get('name'):
                                    lines.append((0, 0, {'product_id': product.id, 'product_qty': 1}))
                                    qty = None
                            mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                          'code': self.vault_revision,
                                                          'product_qty': 1,
                                                          'type': 'normal',
                                                          'routing_id': mrp_routing.id or None,
                                                          'bom_line_ids': lines,
                                                          })

                    # Código A10
                    elif vals['vault_code'] == 'A10':
                        parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                        categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                     ('parent_id', '=', parent_categ.id)])
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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                                        vals.get('product_color')
                                         })

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:
                            qty = ''
                            if vals.get('vault_material_code') or vals['vault_edge_code'] or vals['vault_color']:
                                lines = []
                                if vals['vault_material_code']:
                                    product = self.env['product.product']. \
                                        search([('default_code', '=', vals['vault_material_code'])])
                                    if product.categ_base == 'MADERA':
                                        if 'vault_sup_madera' in vals:
                                            qty = vals['vault_sup_madera']
                                    if product:
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                if vals['vault_edge_code']:
                                    product = self.env['product.product']. \
                                        search([('default_code', '=', vals['vault_edge_code']),
                                                ('default_code', '!=', '000000')])
                                    if product.categ_base == 'CANTO':
                                        if 'vault_edge_len' in vals:
                                            qty = vals['vault_edge_len']
                                    if product:
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                if vals['vault_color']:
                                    if 'vault_sup_pintada' in vals:
                                        product = self.env['product.product']. \
                                            search([('default_code', '=', vals['vault_color']),
                                                    ('default_code', '!=', 'I0039Y')])
                                        if product.categ_base == 'COLOR MADERA':
                                            if 'vault_sup_pintada' in vals:
                                                qty = str(vals['vault_sup_pintada'])
                                        if product:
                                            lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                if vals['vault_edge_pin_code']:
                                    if 'vault_edge_painted_sup' in vals:
                                        product = self.env['product.product']. \
                                            search([('default_code', '=', vals['vault_edge_pin_code']),
                                                    ('default_code', '!=', 'I0039Y')])
                                        if product.categ_base == 'COLOR MADERA':
                                            if 'vault_edge_painted_sup' in vals:
                                                qty = str(vals['vault_edge_painted_sup'])
                                        if product:
                                            lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                if len(lines) > 0:
                                    mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                                  'code': self.vault_revision,
                                                                  'product_qty': 1,
                                                                  'type': 'normal',
                                                                  'routing_id': mrp_routing.id or None,
                                                                  'bom_line_ids': lines,
                                                                  })

                    # Código A11
                    elif vals['vault_code'] == 'A11':
                        parent_categ = self.env['product.category'].search([('name', '=', res_code.type)])
                        categ = self.env['product.category'].search([('name', '=', vals['vault_categ']),
                                                                     ('parent_id', '=', parent_categ.id)])
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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        else:
                            vals.update({'description': str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                        vals.get('product_color')})
                        else:
                            vals.update({'description': vals.get('product_color')})

                    # Código A30
                    elif vals['vault_code'] == 'A30' and vals['vault_categ']:
                        if 'is_old_revision' in vals:
                            if vals['is_old_revision']:
                                for rec in self.bom_ids:
                                    rec.is_old_revision = True
                            continue
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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                                        vals.get('product_color')
                                         })

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0 and self.default_code[-3:] == '000':
                            qty = ''
                            if vals.get('vault_material_code'):
                                lines = []
                                product_ids = []
                                if vals['vault_material_code']:
                                    product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                       vals['vault_material_code'])])
                                for product in product_ids:
                                    if vals.get('name'):
                                        qty = 0.0001
                                        if vals['name'][0:3] == 'CPF' or vals['name'][0:3] == 'CPC':
                                            qty = vals['vault_sup_madera']
                                        if vals['name'][0:2] == 'TR' or \
                                                vals['name'][0:2] == 'TC' or \
                                                vals['name'][0:2] == 'TO' or \
                                                vals['name'][0:2] == 'MZ' and 'vault_length_tub' in vals:
                                            if vals['vault_length_tub'] is not None:
                                                qty = float(vals['vault_length_tub']) / 1000
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                        qty = None
                                if len(lines) > 0:
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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                                        vals.get('product_color')
                                         })

                        # Actualiza lista de materiales
                        if len(self.bom_ids) != 0 and self.default_code[-3:] != '000':
                            for line in self.bom_ids[0].bom_line_ids:
                                line.unlink()
                            qty = ''
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
                                    if product.categ_base == 'COLOR METAL':
                                        if 'vault_sup_pintada' in vals:
                                            qty = str(vals['vault_sup_pintada'])
                                    else:
                                        qty = 1
                                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                    qty = None
                                self.bom_ids[0].write({'bom_line_ids': lines})

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0 and self.default_code[-3:] != '000':
                            qty = ''
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
                                    if product.categ_base == 'COLOR METAL':
                                        if 'vault_sup_pintada' in vals:
                                            qty = str(vals['vault_sup_pintada'])
                                    else:
                                        qty = 1
                                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                    qty = None
                                mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                              'product_id': self.product_variant_id.id,
                                                              'code': self.vault_revision,
                                                              'product_qty': 1,
                                                              'type': 'normal',
                                                              'routing_id': mrp_routing.id or None,
                                                              'bom_line_ids': lines,
                                                              'is_vault_bom': False,
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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                                        vals.get('product_color')
                                         })

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

                        if self.vault_material_name and self.product_color:
                            vals.update({'description': str(self.vault_material_name) + ' ' + str(self.product_color)})
                        if vals.get('vault_material_name') and vals.get('product_color'):
                            vals.update({'description': vals.get('vault_material_name') + ' ' +
                                                        vals.get('product_color')
                                         })

                    # Código A50
                    elif vals['vault_code'] == 'A50':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', res_code.route_mrp)])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:
                            if vals.get('vault_purchase_code'):
                                lines = []
                                product_ids = []
                                if vals['vault_purchase_code']:
                                    product_ids = self.env['product.product']. \
                                        search([('default_code', '=', vals['vault_purchase_code'])])
                                for product in product_ids:
                                    if 'vault_length_cut' in vals and vals['vault_length_cut'] != 0:
                                        qty = vals['vault_length_cut']
                                    else:
                                        qty = 1
                                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                              'code': self.vault_revision,
                                                              'product_qty': 1,
                                                              'type': 'normal',
                                                              'routing_id': mrp_routing.id or None,
                                                              'bom_line_ids': lines,
                                                              })

                    # Código A70
                    elif vals['vault_code'] == 'A70':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:

                            if vals.get('vault_purchase_code') or vals['vault_left_hand'] or vals['vault_right_hand']:
                                lines = []
                                product_ids = []
                                if vals['vault_purchase_code']:
                                    product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                       vals[
                                                                                           'vault_purchase_code'])])
                                if vals['vault_left_hand']:
                                    product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                        vals[
                                                                                            'vault_left_hand'])])
                                if vals['vault_right_hand']:
                                    product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                        vals[
                                                                                            'vault_right_hand'])])
                                for product in product_ids:
                                    qty = 0.0
                                    if vals.get('vault_length_tub'):
                                        if vals['vault_length_tub'] is not None:
                                            qty = float(vals['vault_length_tub']) / 1000
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                    else:
                                        qty = 1
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                              'code': self.vault_revision,
                                                              'product_qty': 1,
                                                              'type': 'normal',
                                                              'routing_id': None,
                                                              'bom_line_ids': lines,
                                                              })
                    # Código A72
                    elif vals['vault_code'] == 'A72':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:

                            if vals.get('vault_purchase_code') or vals['vault_left_hand'] or vals['vault_right_hand']:
                                lines = []
                                product_ids = []
                                if vals['vault_purchase_code']:
                                    product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                       vals[
                                                                                           'vault_purchase_code'])])
                                if vals['vault_left_hand']:
                                    product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                        vals[
                                                                                            'vault_left_hand'])])
                                if vals['vault_right_hand']:
                                    product_ids += self.env['product.product'].search([('default_code', '=',
                                                                                        vals[
                                                                                            'vault_right_hand'])])
                                for product in product_ids:
                                    qty = 0.0
                                    if vals.get('vault_length_tub'):
                                        if vals['vault_length_tub'] is not None:
                                            qty = float(vals['vault_length_tub']) / 1000
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                    else:
                                        qty = 1
                                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                              'code': self.vault_revision,
                                                              'product_qty': 1,
                                                              'type': 'normal',
                                                              'routing_id': mrp_routing.id or None,
                                                              'bom_line_ids': lines,
                                                              })
                    # Código A90
                    elif vals['vault_code'] == 'A90':
                        # Check si existe ruta
                        mrp_routing = self.env['mrp.routing'].search([('name', '=', vals['vault_route'])])
                        if vals['vault_route'] and not len(mrp_routing):
                            raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                                    % (vals['vault_route'], vals['name'])))

                        # Crear lista de materiales
                        if len(self.bom_ids) == 0:

                            if vals.get('vault_purchase_code'):
                                lines = []
                                product_ids = []
                                if vals['vault_purchase_code']:
                                    product_ids = self.env['product.product'].search([('default_code', '=',
                                                                                       vals[
                                                                                           'vault_purchase_code'])])
                                for product in product_ids:
                                    if 'vault_sup_madera' in vals and vals['vault_sup_madera'] != 0:
                                        qty = vals['vault_sup_madera']
                                    else:
                                        qty = 1
                                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                                mrp_bom_object.sudo().create({'product_tmpl_id': self.id,
                                                              'code': self.vault_revision,
                                                              'product_qty': 1,
                                                              'type': 'normal',
                                                              'routing_id': mrp_routing.id or None,
                                                              'bom_line_ids': lines,
                                                              })

                    # Para valores predeterminados
                    if res_code.route_mrp:
                        vals.update({'vault_route': res_code.route_mrp})
                    if res_code.categ_fixed:
                        vals.update({'categ_id': res_code.categ_fixed.id})
                    if res_code.uom_dimensions:
                        vals.update({'dimensional_uom_id': res_code.uom_dimensions.id})
            # print(self.categ_id.name, record.categ_id.name, self.name, record.name)
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
            elif vals.get('default_code')[0:3] == 'A60' and vals.get('default_code')[-6:-5] == 'V':
                var = vals['default_code'][0:3] + 'V'
            elif vals.get('default_code')[0:3] == 'A60' and vals.get('default_code')[-6:-5] == 'S':
                var = vals['default_code'][0:3] + 'S'
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
