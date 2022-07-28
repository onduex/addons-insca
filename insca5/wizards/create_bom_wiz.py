# -*- coding: utf-8 -*-
# © 2019 Sergio Díaz (<sdimar@yahoo.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CreateBomWiz(models.TransientModel):
    _name = 'create.bom.wiz'

    product_id = fields.Many2one(
        comodel_name='product.template', string="Producto",
        help="Producto a embalar", ondelete='cascade', readonly=True)
    embalaje_id = fields.Many2one(
        comodel_name='product.template', string="Producto",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    embalaje_bom = fields.Many2one(
        comodel_name='mrp.bom', string="LdM",
        help="Producto embalaje.", ondelete='cascade', readonly=True)
    largo = fields.Integer(string='Largo', required=False)
    ancho = fields.Integer(string='Ancho', required=False)
    alto = fields.Integer(string='Alto', required=False)
    espesor_base = fields.Integer(string='Espesor base', required=False)
    n_tacos = fields.Integer(string='Nº de tacos', required=False)

    tapa = fields.Char(string='Tapa', required=False, readonly=True)
    base = fields.Char(string='Base', required=False, readonly=True)
    l_largo = fields.Char(string='Lateral largo', required=False, readonly=True)
    l_corto = fields.Char(string='Lateral corto', required=False, readonly=True)
    taco = fields.Char(string='Taco', required=False, readonly=True)

    tapa_id = fields.Integer(string='Tapa', required=False, readonly=True)
    base_id = fields.Integer(string='Base', required=False, readonly=True)
    l_largo_id = fields.Integer(string='Lateral largo', required=False, readonly=True)
    l_corto_id = fields.Integer(string='Lateral corto', required=False, readonly=True)
    taco_id = fields.Integer(string='Taco', required=False, readonly=True)

    @api.onchange('largo', 'ancho', 'alto', 'espesor_base', 'n_tacos')
    def onchange_values(self):
        self.tapa = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.ancho) + 'X' + '16mm'
        self.base = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.ancho) + 'X' + str(self.espesor_base) + 'mm'
        self.l_largo = 'PIEZA EMBALAJE ' + str(self.largo) + 'X' + str(self.alto) + 'X' + '16mm'
        self.l_corto = 'PIEZA EMBALAJE ' + str(self.alto) + 'X' + str(self.ancho) + 'X' + '16mm'
        self.taco = 'TACO ' + '80X80mm'

        self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
        self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)])

    def create_bom(self):
        self.onchange_values()
        product_ids = []
        lines = []
        product_tmpl_obj = self.env['product.template']
        if self.largo == 0 or \
                self.ancho == 0 or \
                self.alto == 0 or \
                self.espesor_base == 0 or \
                self.n_tacos == 0:
            raise ValidationError(_('¡Obligatorio todas las dimensiones distintas de cero!'))

        # Tapa
        self.tapa_id = self.env["product.template"].search([("name", "=", self.tapa)])
        if self.tapa_id:
            product_ids.append({'id': self.tapa_id,
                                'qty': 1,
                                })
        if not self.tapa_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.tapa,
                                                               'default_code': 'EM01.' + self.embalaje_id.default_code[4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': 1,
                                })

        # Base
        self.base_id = self.env["product.template"].search([("name", "=", self.base)])
        if self.base_id:
            product_ids.append({'id': self.base_id,
                                'qty': 1,
                                })
        if not self.base_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.base,
                                                               'default_code': 'EM02.' + self.embalaje_id.default_code[4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': 1,
                                })

        # Lateral largo
        self.l_largo_id = self.env["product.template"].search([("name", "=", self.l_largo)])
        if self.l_largo_id:
            product_ids.append({'id': self.l_largo_id,
                                'qty': 2,
                                })
        if not self.l_largo_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.l_largo,
                                                               'default_code': 'EM03.' + self.embalaje_id.default_code[4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': 2,
                                })

        # Lateral corto
        self.l_corto_id = self.env["product.template"].search([("name", "=", self.l_corto)])
        if self.l_corto_id:
            product_ids.append({'id': self.l_corto_id,
                                'qty': 2,
                                })
        if not self.l_corto_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.l_corto,
                                                               'default_code': 'EM04.' + self.embalaje_id.default_code[4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': 2,
                                })

        # Taco
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)])
        if self.taco_id:
            product_ids.append({'id': self.taco_id,
                                'qty': self.n_tacos,
                                })
        if not self.taco_id:
            product_ids.append({'id': product_tmpl_obj.create({'name': self.taco,
                                                               'default_code': 'EM05.' + self.embalaje_id.default_code[4:],
                                                               'type': "product",
                                                               'categ_id': self.embalaje_id.categ_id.id,
                                                               'sale_ok': False,
                                                               'purchase_ok': False,
                                                               }).id,
                                'qty': self.n_tacos,
                                })

        if self.embalaje_bom.bom_line_ids:
            raise ValidationError(_('¡Esta LdM no está vacía, comprobar!'))
        else:
            for rec in product_ids:
                product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec['id'])]).id
                exist = self.env['mrp.bom.line'].search([('bom_id', '=', self.embalaje_bom.id),
                                                         ('product_id', '=', product_id)])

                if not exist:
                    self.env['mrp.bom.line'].sudo().create({'bom_id': self.embalaje_bom.id,
                                                            'product_id': product_id,
                                                            'product_qty': rec['qty']})
                else:
                    exist.update({'product_qty': exist['product_qty'] + rec['qty']})
                                                                                                 

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def create_bom_wiz_action(self):
        embalaje_id = self.env["product.template"].search([("default_code", "ilike",
                                                            'EM0.' + self.default_code[4:10])])
        embalaje_bom = self.env["mrp.bom"].search([("product_tmpl_id", "=", embalaje_id.id)])

        context = {'default_product_id': self.id,
                   'default_embalaje_id': embalaje_id.id,
                   'default_embalaje_bom': max(embalaje_bom).id,
                   }
        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
