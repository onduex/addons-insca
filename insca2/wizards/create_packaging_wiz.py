# -*- coding: utf-8 -*-
# © 2019 Sergio Díaz (<sdimar@yahoo.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CreatePackagingWiz(models.TransientModel):
    _name = 'create.packaging.wiz'
    _description = 'Wizard para crear LdM de embalajes'

    product_id = fields.Many2one(
        comodel_name='product.template', string="Producto",
        help="Producto a embalar", ondelete='cascade', readonly=True)
    embalaje_id = fields.Many2one(
        comodel_name='product.template', string="Embalaje",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    embalaje_bom = fields.Many2one(
        comodel_name='mrp.bom', string="LdM",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    n_bulto_lines = fields.Integer(string='Nº de bulto', required=False, compute='onchange_values')
    largo = fields.Integer(string='Largo', required=False, readonly=True)
    ancho = fields.Integer(string='Ancho', required=False, readonly=True)
    alto = fields.Integer(string='Alto', required=False, readonly=True)
    largo_exterior = fields.Integer(string='Largo exterior', required=False)
    ancho_exterior = fields.Integer(string='Ancho exterior', required=False)
    alto_exterior = fields.Integer(string='Alto exterior', required=False)
    espesor_general = fields.Selection(string='Espesor general', selection=[('16', '16'), ('19', '19'), ],
                                       required=False, )
    espesor_base = fields.Selection(string='Espesor base', selection=[('25', '25'), ('30', '30'), ], required=False, )
    tipo_palet = fields.Selection(string='Tipo palet', selection=[('0', 'Sin mordida'), ('1', 'Con mordida'),
                                                                  ('2', 'Sólo base'), ('4', 'Pequeño'),
                                                                  ('5', 'Pequeño sólo base')],
                                  required=False, )

    n_tacos = fields.Integer(string='Nº tacos', required=False, readonly=True)
    n_tacos_lateral = fields.Integer(string='Nº tacos lateral', required=False, readonly=True)
    n_tacos_costado = fields.Integer(string='Nº tacos costado', required=False, readonly=True)
    n_bultos = fields.Integer(string='Nº de bultos iguales', required=False, default=1)
    largo_taco = fields.Integer(string='Largo taco', required=False, readonly=True)
    largo_taco_lateral = fields.Integer(string='Largo taco lateral', required=False, readonly=True)
    largo_taco_costado = fields.Integer(string='Largo taco costado', required=False, readonly=True)

    bulto = fields.Char(string='Bulto', required=False, readonly=True)
    tapa = fields.Char(string='Tapa', required=False, readonly=True)
    base = fields.Char(string='Base', required=False, readonly=True)
    l_largo = fields.Char(string='Lateral largo', required=False, readonly=True)
    l_corto = fields.Char(string='Lateral corto', required=False, readonly=True)
    taco = fields.Char(string='Taco', required=False, readonly=True)
    taco_lateral = fields.Char(string='Taco lateral', required=False, readonly=True)
    taco_costado = fields.Char(string='Taco costado', required=False, readonly=True)

    tapa_id = fields.Integer(string='Tapa Id', required=False, readonly=True)
    base_id = fields.Integer(string='Base Id', required=False, readonly=True)
    l_largo_id = fields.Integer(string='Lateral largo Id', required=False, readonly=True)
    l_corto_id = fields.Integer(string='Lateral corto Id', required=False, readonly=True)
    taco_id = fields.Integer(string='Taco Id', required=False, readonly=True)
    taco_lateral_id = fields.Integer(string='Taco lateral Id', required=False, readonly=True)
    taco_costado_id = fields.Integer(string='Taco costado Id', required=False, readonly=True)

    @api.onchange('largo_exterior', 'ancho_exterior', 'alto_exterior', 'espesor_general', 'espesor_base', 'tipo_palet')
    def onchange_medidas_exteriores(self):
        alto_tacos = self.env["res.packaging"].search([("name", "=", 'Alto tacos')]).value
        self.largo = self.largo_exterior - (2 * int(self.espesor_general)) - 1
        self.ancho = self.ancho_exterior - (2 * int(self.espesor_general)) - 1
        if self.tipo_palet != "4" and self.tipo_palet != "5":
            self.alto = self.alto_exterior - int(self.espesor_general) - alto_tacos - 10
        else:
            self.alto = self.alto_exterior - int(self.espesor_general) - int(self.espesor_base) - alto_tacos

    @api.onchange('largo_exterior', 'ancho_exterior', 'alto_exterior', 'largo', 'ancho', 'espesor_general', 'tipo_palet')
    def onchange_largo_taco(self):
        sep_taco_lateral = self.env["res.packaging"].search([("name", "=", 'Separación taco lateral')]).value
        l_taco_lateral = self.env["res.packaging"].search([("name", "=", 'Largo taco lateral')]).value
        a = 2 * int(self.espesor_general)
        b = 2 * sep_taco_lateral

        # Cálculo taco principal
        if 0 < self.largo < 750:
            if self.tipo_palet != "4" and self.tipo_palet != "5":
                self.largo_exterior = 0
                raise UserError(_('Largo minimo 750mm vs %smm, debe usar tipo de palet pequeño' % self.largo))
        elif 750 <= self.largo <= 1350:
            self.largo_taco = l_taco_lateral
        elif self.largo > 1350:
            self.largo_taco = (a + self.largo - b - l_taco_lateral) / 2

        # Cálculo taco lateral
        if self.largo >= 800 and (self.tipo_palet != "4" and self.tipo_palet != "5"):
            self.n_tacos_lateral = 2
            self.largo_taco_lateral = l_taco_lateral
        else:
            self.n_tacos_lateral = 0
            self.largo_taco_lateral = 0

        # Cálculo taco costado
        if 0 < self.ancho < 750:
            if self.tipo_palet != "4" and self.tipo_palet != "5":
                self.ancho_exterior = 0
                raise UserError(_('Ancho minimo 750mm vs %smm, debe usar tipo de palet pequeño' % self.ancho))
            else:
                # largo taco para tipo de palet pequeño
                self.largo_taco = self.ancho
        if self.ancho >= 800 and (self.tipo_palet != "4" and self.tipo_palet != "5"):
            self.n_tacos_costado = 2
            self.largo_taco_costado = self.largo_taco - 100
        else:
            self.n_tacos_costado = 0
            self.largo_taco_costado = 0

    @api.onchange('largo', 'ancho', 'alto', 'espesor_base', 'espesor_general', 'n_tacos', 'n_bultos', 'tipo_palet')
    def onchange_values(self):

        alto_tacos = self.env["res.packaging"].search([("name", "=", 'Alto tacos')]).value
        ancho_tacos = self.env["res.packaging"].search([("name", "=", 'Ancho tacos')]).value
        distancia_suelo = self.env["res.packaging"].search([("name", "=", 'Distancia al suelo del lateral')]).value

        if self.tipo_palet != "4" and self.tipo_palet != "5":
            self.n_tacos = self.env["res.packaging"].search([("name", "=", 'Número de tacos')]).value
        elif (self.tipo_palet == "4" or self.tipo_palet == "5") and self.largo_exterior < 1000:
            self.n_tacos = 2
        elif (self.tipo_palet == "4" or self.tipo_palet == "5") and self.largo_exterior >= 1000:
            self.n_tacos = 3

        self.n_bulto_lines = len(self.embalaje_bom.bom_line_ids)

        self.bulto = 'BULTO ' + str(self.largo_exterior).zfill(4) \
                     + 'x' + str(self.ancho_exterior).zfill(4) \
                     + 'x' + str(self.alto_exterior).zfill(4) + 'mm'
        self.tapa = self.get_major_dimension_type_one(self.largo_exterior, self.ancho_exterior, self.espesor_general)
        self.base = self.get_major_dimension_type_two(self.largo, self.ancho, self.espesor_base)
        self.l_largo = self.get_major_dimension_type_three(self.largo, self.alto, self.espesor_general, alto_tacos,
                                                           self.espesor_base, distancia_suelo, self.tipo_palet)
        self.l_corto = self.get_major_dimension_type_four(self.alto, self.ancho, self.espesor_general, self.tipo_palet,
                                                          self.espesor_base, alto_tacos)
        self.taco = 'TACO PINO PAIS ' + str(alto_tacos).zfill(3) + 'x' + str(ancho_tacos).zfill(3) + 'x' + \
                    str(self.largo_taco).zfill(4) + 'mm'
        self.taco_lateral = 'TACO PINO PAIS ' + str(alto_tacos).zfill(3) + 'x' + str(ancho_tacos).zfill(3) + 'x' + \
                            str(self.largo_taco_lateral).zfill(4) + 'mm'
        self.taco_costado = 'TACO PINO PAIS ' + str(alto_tacos).zfill(3) + 'x' + str(ancho_tacos).zfill(3) + 'x' + \
                            str(self.largo_taco_costado).zfill(4) + 'mm'

        self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
        self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)])
        self.taco_lateral_id = self.env["product.template"].search([("name", "=", self.taco_lateral)])
        self.taco_costado_id = self.env["product.template"].search([("name", "=", self.taco_costado)])

    def create_bom(self):
        alto_tacos = self.env["res.packaging"].search([("name", "=", 'Alto tacos')]).value
        ancho_tacos = self.env["res.packaging"].search([("name", "=", 'Ancho tacos')]).value
        distancia_suelo = self.env["res.packaging"].search([("name", "=", 'Distancia al suelo del lateral')]).value
        self.onchange_medidas_exteriores()
        self.onchange_largo_taco()
        self.onchange_values()
        product_ids = []
        product_tmpl_obj = self.env['product.template']
        mrp_bom_obj = self.env['mrp.bom']
        bulto_weight = 0.0

        if not self.tipo_palet:
            raise ValidationError(
                _('¡Obligatorio Tipo de palet definido'))
        else:
            if self.tipo_palet != "2":
                if self.largo_exterior == 0 or \
                        self.ancho_exterior == 0 or \
                        self.alto_exterior == 0 or \
                        self.espesor_base == 0 or \
                        self.espesor_general == 0 or \
                        self.n_bultos == 0:
                    raise ValidationError(
                        _('¡Obligatorio todas las dimensiones distintas de cero!'))
            else:
                if self.largo_exterior == 0 or \
                        self.ancho_exterior == 0 or \
                        self.espesor_base == 0:
                    raise ValidationError(
                        _('¡Obligatorio todas las dimensiones activas distintas de cero!'))

        # Crear primer nivel de embalaje
        if len(self.embalaje_bom.bom_line_ids) < 10:
            default_code = 'B0' + str(len(self.embalaje_bom.bom_line_ids) + 1) + '.' + self.embalaje_id.default_code[4:]
        else:
            default_code = 'B' + str(len(self.embalaje_bom.bom_line_ids) + 1) + '.' + self.embalaje_id.default_code[4:]
        bulto_id = self.env["product.template"].search([("default_code", "=", default_code)])
        if bulto_id:
            raise ValidationError(
                _('El bulto %s ya existe' % bulto_id['default_code']))
        # Crear nuevo bulto
        new_id = product_tmpl_obj.create({'name': self.bulto,
                                          'default_code': default_code,
                                          'type': "product",
                                          'categ_id': self.embalaje_id.categ_id.id,
                                          'sale_ok': False,
                                          'purchase_ok': False,
                                          'product_length': float(self.largo_exterior) / 1000,
                                          'product_width': float(self.ancho_exterior) / 1000,
                                          'product_height': float(self.alto_exterior) / 1000,
                                          'volume': (float(self.largo_exterior) / 1000 *
                                                     float(self.ancho_exterior) / 1000 *
                                                     float(self.alto_exterior) / 1000
                                                     ),
                                          'product_package_number': self.n_bultos,
                                          'route_ids': [(6, 0, [x for x in (1, 5)])]
                                          })['id']
        product_obj = self.env['product.product'].search([('product_tmpl_id', '=', new_id)])
        # Crear LdM del bulto
        new_bom_id = mrp_bom_obj.sudo().create({'product_tmpl_id': new_id,
                                                'product_id': product_obj.id,
                                                'product_qty': 1,
                                                'type': 'phantom',
                                                # 'routing_id': 141,  # SEC-EMB
                                                })
        # Crear bulto como línea de LdM
        self.env['mrp.bom.line'].sudo().create({'bom_id': self.embalaje_bom.id,
                                                'product_id': product_obj.id,
                                                'product_qty': self.n_bultos})

        # Base
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        if self.base_id:
            product_ids.append({'id': self.base_id,
                                'qty': 1,
                                'name': self.base,
                                'vault_route': 'SEC'
                                })
        if not self.base_id:
            default_code = self.get_major_code_type_two(self.largo, self.ancho, self.espesor_base)
            volume = float(default_code[:4]) / 1000 * float(default_code[4:8]) / 1000 * float(default_code[8:]) / 1000
            product_ids.append({'id': product_tmpl_obj.create({'name': self.base,
                                                               'default_code': default_code,
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'product_length': float(default_code[:4]) / 1000,
                                                               'product_width': float(default_code[4:8]) / 1000,
                                                               'product_height': float(default_code[8:]) / 1000,
                                                               'volume': volume,
                                                               'weight': volume * 670,
                                                               'vault_material_code': 'VT.00AAM0'
                                                                                      + str(self.espesor_base) + 'mm',
                                                               'vault_sup_madera': str(float(default_code[:4]) / 1000 *
                                                                                       float(default_code[4:8]) / 1000),
                                                               'vault_route': 'SEC',
                                                               'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                               }).id,
                                'qty': 1,
                                'name': self.base,
                                'vault_route': 'SEC'
                                })

        # Taco
        taco_material = self.env["res.packaging"].search([("name", "=", 'Material tacos')]).code
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)])
        if self.taco_id:
            product_ids.append({'id': self.taco_id,
                                'qty': self.n_tacos,
                                'name': self.taco,
                                'vault_route': 'MAN'
                                })
        if not self.taco_id:
            default_code = 'TC.' + str(alto_tacos).zfill(3) + str(ancho_tacos).zfill(3) + str(self.largo_taco).zfill(4)
            volume = float(default_code[9:]) / 1000 * float(default_code[6:9]) / 1000 * float(default_code[3:6]) / 1000
            product_ids.append({'id': product_tmpl_obj.create({'name': self.taco,
                                                               'default_code': default_code,
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               'product_length': float(default_code[9:]) / 1000,
                                                               'product_width': float(default_code[6:9]) / 1000,
                                                               'product_height': float(default_code[3:6]) / 1000,
                                                               'volume': volume,
                                                               'weight': volume * 490,
                                                               'vault_material_code': taco_material,
                                                               'vault_sup_madera': str(float(alto_tacos) *
                                                                                       float(ancho_tacos) *
                                                                                       float(self.largo_taco)
                                                                                       / 1000000000),
                                                               'vault_route': 'MAN',
                                                               'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                               }).id,
                                'qty': self.n_tacos,
                                'name': self.taco,
                                'vault_route': 'MAN'
                                })

        # Taco lateral
        if self.n_tacos_lateral:
            self.taco_lateral_id = self.env["product.template"].search([("name", "=", self.taco_lateral)])
            if self.taco_lateral_id:
                product_ids.append({'id': self.taco_lateral_id,
                                    'qty': self.n_tacos_lateral,
                                    'name': self.taco_lateral,
                                    'vault_route': 'MAN'
                                    })
            if not self.taco_lateral_id:
                default_code = ('TC.' + str(alto_tacos).zfill(3) + str(ancho_tacos).zfill(3) +
                                str(self.largo_taco).zfill(4))
                volume = float(default_code[9:]) / 1000 * float(default_code[6:9]) / 1000 * float(
                    default_code[3:6]) / 1000
                product_ids.append({'id': product_tmpl_obj.create({'name': self.taco_lateral,
                                                                   'default_code': default_code,
                                                                   'type': "product",
                                                                   'categ_id': self.embalaje_id.categ_id.id,
                                                                   'sale_ok': False,
                                                                   'purchase_ok': False,
                                                                   'product_length': float(default_code[9:]) / 1000,
                                                                   'product_width': float(default_code[6:9]) / 1000,
                                                                   'product_height': float(default_code[3:6]) / 1000,
                                                                   'volume': volume,
                                                                   'weight': volume * 490,
                                                                   'vault_material_code': taco_material,
                                                                   'vault_sup_madera': str(float(alto_tacos) *
                                                                                           float(ancho_tacos) *
                                                                                           float(
                                                                                               self.largo_taco_lateral)
                                                                                           / 1000000000),
                                                                   'vault_route': 'MAN',
                                                                   'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                                   }).id,
                                    'qty': self.n_tacos_lateral,
                                    'name': self.taco_lateral,
                                    'vault_route': 'MAN'
                                    })

        # Taco costado
        if self.n_tacos_costado:
            self.taco_costado_id = self.env["product.template"].search([("name", "=", self.taco_costado)])
            if self.taco_costado_id:
                product_ids.append({'id': self.taco_costado_id,
                                    'qty': self.n_tacos_costado,
                                    'name': self.taco_costado,
                                    'vault_route': 'MAN'
                                    })
            if not self.taco_costado_id:
                default_code = ('TC.' + str(alto_tacos).zfill(3) + str(ancho_tacos).zfill(3) +
                                str(self.largo_taco_costado).zfill(4))
                volume = float(default_code[9:]) / 1000 * float(default_code[6:9]) / 1000 * float(
                    default_code[3:6]) / 1000
                product_ids.append({'id': product_tmpl_obj.create({'name': self.taco_costado,
                                                                   'default_code': default_code,
                                                                   'type': "product",
                                                                   'categ_id': self.embalaje_id.categ_id.id,
                                                                   'sale_ok': False,
                                                                   'purchase_ok': False,
                                                                   'product_length': float(default_code[9:]) / 1000,
                                                                   'product_width': float(default_code[6:9]) / 1000,
                                                                   'product_height': float(default_code[3:6]) / 1000,
                                                                   'volume': volume,
                                                                   'weight': volume * 490,
                                                                   'vault_material_code': taco_material,
                                                                   'vault_sup_madera': str(float(alto_tacos) *
                                                                                           float(ancho_tacos) *
                                                                                           float(
                                                                                               self.largo_taco_costado)
                                                                                           / 1000000000),
                                                                   'vault_route': 'MAN',
                                                                   'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                                   }).id,
                                    'qty': self.n_tacos_costado,
                                    'name': self.taco_costado,
                                    'vault_route': 'MAN'
                                    })

        # Si el tipo palet != solo base
        if self.tipo_palet != "2":

            # Tapa
            self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
            if self.tapa_id:
                product_ids.append({'id': self.tapa_id,
                                    'qty': 1,
                                    'name': self.tapa,
                                    'vault_route': 'SEC'
                                    })
            if not self.tapa_id:
                default_code = self.get_major_code_type_one(self.largo_exterior, self.ancho_exterior,
                                                            self.espesor_general)
                volume = float(default_code[:4]) / 1000 * float(default_code[4:8]) / 1000 * float(
                    default_code[8:]) / 1000
                product_ids.append({'id': product_tmpl_obj.create({'name': self.tapa,
                                                                   'default_code': default_code,
                                                                   'type': "product",
                                                                   'categ_id': self.embalaje_id.categ_id.id,
                                                                   'sale_ok': False,
                                                                   'purchase_ok': False,
                                                                   'product_length': float(default_code[:4]) / 1000,
                                                                   'product_width': float(default_code[4:8]) / 1000,
                                                                   'product_height': float(default_code[8:]) / 1000,
                                                                   'volume': volume,
                                                                   'weight': volume * 670,
                                                                   'vault_material_code': 'VT.00AAM0'
                                                                                          + str(self.espesor_general)
                                                                                          + 'mm',
                                                                   'vault_sup_madera': str(
                                                                       float(default_code[:4]) / 1000 *
                                                                       float(default_code[4:8]) / 1000),
                                                                   'vault_route': 'SEC',
                                                                   'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                                   }).id,
                                    'qty': 1,
                                    'name': self.tapa,
                                    'vault_route': 'SEC'
                                    })

            # Lateral largo
            self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
            if self.l_largo_id:
                product_ids.append({'id': self.l_largo_id,
                                    'qty': 2,
                                    'name': self.l_largo,
                                    'vault_route': 'SEC'
                                    })
            if not self.l_largo_id:
                default_code = self.get_major_code_type_three(self.largo, self.alto, self.espesor_general,
                                                              alto_tacos, self.espesor_base, distancia_suelo,
                                                              self.tipo_palet)
                volume = float(default_code[:4]) / 1000 * float(default_code[4:8]) / 1000 * float(
                    default_code[8:]) / 1000
                product_ids.append({'id': product_tmpl_obj.create({'name': self.l_largo,
                                                                   'default_code': default_code,
                                                                   'type': "product",
                                                                   'categ_id': self.embalaje_id.categ_id.id,
                                                                   'sale_ok': False,
                                                                   'purchase_ok': False,
                                                                   'product_length': float(default_code[:4]) / 1000,
                                                                   'product_width': float(default_code[4:8]) / 1000,
                                                                   'product_height': float(default_code[8:]) / 1000,
                                                                   'volume': volume,
                                                                   'weight': volume * 670,
                                                                   'vault_material_code': 'VT.00AAM0'
                                                                                          + str(self.espesor_general)
                                                                                          + 'mm',
                                                                   'vault_sup_madera': str(
                                                                       float(default_code[:4]) / 1000 *
                                                                       float(default_code[4:8]) / 1000),
                                                                   'vault_route': 'SEC',
                                                                   'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                                   }).id,
                                    'qty': 2,
                                    'name': self.l_largo,
                                    'vault_route': 'SEC'
                                    })

            # Lateral corto
            self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
            if self.l_corto_id:
                product_ids.append({'id': self.l_corto_id,
                                    'qty': 2,
                                    'name': self.l_corto,
                                    'vault_route': 'SEC'
                                    })
            if not self.l_corto_id:
                default_code = self.get_major_code_type_four(self.alto, self.ancho, self.espesor_general,
                                                             self.tipo_palet, self.espesor_base, alto_tacos)
                volume = float(default_code[:4]) / 1000 * float(default_code[4:8]) / 1000 * float(
                    default_code[8:]) / 1000
                product_ids.append({'id': product_tmpl_obj.create({'name': self.l_corto,
                                                                   'default_code': default_code,
                                                                   'type': "product",
                                                                   'categ_id': self.embalaje_id.categ_id.id,
                                                                   'sale_ok': False,
                                                                   'purchase_ok': False,
                                                                   'product_length': float(default_code[:4]) / 1000,
                                                                   'product_width': float(default_code[4:8]) / 1000,
                                                                   'product_height': float(default_code[8:]) / 1000,
                                                                   'volume': volume,
                                                                   'weight': volume * 670,
                                                                   'vault_material_code': 'VT.00AAM0'
                                                                                          + str(self.espesor_general)
                                                                                          + 'mm',
                                                                   'vault_sup_madera': str(
                                                                       float(default_code[:4]) / 1000 *
                                                                       float(default_code[4:8]) / 1000),
                                                                   'vault_route': 'SEC',
                                                                   'route_ids': [(6, 0, [x for x in (1, 5)])]
                                                                   }).id,
                                    'qty': 2,
                                    'name': self.l_corto,
                                    'vault_route': 'SEC'
                                    })

        # Crear las líneas de la LdM del bulto
        for rec in product_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec['id'])]).id
            exist = self.env['mrp.bom.line'].search([('bom_id', '=', new_bom_id.id),
                                                     ('product_id', '=', product_id)])

            if not exist:
                self.env['mrp.bom.line'].sudo().create({'bom_id': new_bom_id.id,
                                                        'product_id': product_id,
                                                        'product_qty': rec['qty']})
            else:
                exist.update({'product_qty': exist['product_qty'] + rec['qty']})

            # Sumatorio de los pesos de los productos
            bulto_weight += (rec['qty'] * self.env['product.product'].
                             search([('product_tmpl_id', '=', rec['id'])]).weight)

        bulto_obj = self.env['product.template'].search([('id', '=', new_id)])
        bulto_obj.write({'weight': bulto_weight})

        # Crear las LdM de los materiales y su consumo de material prima
        for record in product_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', record['id'])]).id
            product_tmpl = self.env['product.template'].search([('id', '=', record['id'])])
            raw_material = self.env['product.product'].search(
                [('default_code', '=', product_tmpl['vault_material_code'])])
            routing_id = self.env["mrp.routing"].search([("name", "=", record['vault_route'])]).id
            if not product_tmpl.bom_ids:
                new2_bom_id = mrp_bom_obj.sudo().create({'product_tmpl_id': record['id'],
                                                         'product_id': product_id,
                                                         'product_qty': 1,
                                                         'type': 'normal',
                                                         'routing_id': routing_id
                                                         })
                if len(raw_material) == 1:
                    self.env['mrp.bom.line'].sudo().create({'bom_id': new2_bom_id.id,
                                                            'product_id': raw_material.id,
                                                            'product_qty':
                                                                float(new2_bom_id.product_tmpl_id.vault_sup_madera)
                                                            })

        self.n_bultos = 1
        self.largo = 0
        self.ancho = 0
        self.alto = 0
        self.largo_exterior = 0
        self.ancho_exterior = 0
        self.alto_exterior = 0

        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.packaging.wiz',
            'context': self.env.context,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new'}


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def create_bom_wiz_action(self):
        product_tmpl_obj = self.env["product.template"]
        mrp_bom_obj = self.env["mrp.bom"]
        res_code = self.env['res.code'].search([('name', '=', self.default_code[:3])])
        embalaje_id = self.env["product.template"]. \
                      search([("default_code", "ilike", 'EM0.' + self.default_code[4:17])])
        embalaje_bom = self.env["mrp.bom"].search([("product_tmpl_id", "=", embalaje_id.id)])

        # Si no encuentra el embalaje, lo crea
        if not embalaje_id:
            embalaje_id = product_tmpl_obj.create({'name': 'EMBALAJE',
                                                   'default_code': 'EM0.' + self.default_code[4:17],
                                                   'type': res_code.type_store,
                                                   'categ_id': 2552,  # EMBALAJE
                                                   'sale_ok': res_code.sale_ok,
                                                   'purchase_ok': res_code.purchase_ok,
                                                   'route_ids': [(6, 0, [x.id for x in res_code.product_route_ids])],
                                                   })
        # Si no encuentra la ldM del embalaje, la crea
        if not embalaje_bom:
            embalaje_bom = mrp_bom_obj.sudo().create({'product_tmpl_id': embalaje_id.id,
                                                      'product_qty': 1,
                                                      'type': 'phantom',
                                                      'routing_id': res_code.route_mrp or None,
                                                      })
        # Crear embalaje como línea de LdM
        if embalaje_id:
            embalaje_variant_id = self.env["product.product"]. \
                                  search([("default_code", "ilike", 'EM0.' + self.default_code[4:17])])

            embalaje_as_bom_line_id = self.env['mrp.bom.line']. \
                                      search([("product_id", "ilike", 'EM0.' + self.default_code[4:17]),
                                              ("bom_id", "ilike", self.bom_ids[0].id)])
            if not embalaje_as_bom_line_id:
                self.env['mrp.bom.line'].sudo().create({'bom_id': self.bom_ids[0].id,
                                                        'product_id': embalaje_variant_id.id,
                                                        'product_qty': 1,
                                                        })

        context = {'default_product_id': self.id,
                   'default_embalaje_id': embalaje_id.id,
                   'default_embalaje_bom': max(embalaje_bom).id or None,
                   }
        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.packaging.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
