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
        self.taco_id = self.env["product.template"].search([("name", "=", self.taco)]).id


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def create_bom_wiz_action(self):
        embalaje_id = self.env["product.template"].search([("default_code", "ilike",
                                                            'EM0.' + self.default_code[4:10])])
        context = {'default_product_id': self.id,
                   'default_embalaje_id': embalaje_id.id}
        return {
            'name': 'Crear embalaje',
            'type': 'ir.actions.act_window',
            'res_model': 'create.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
