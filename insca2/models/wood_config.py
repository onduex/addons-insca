# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WoodConfig(models.Model):
    _name = "wood.config"
    _description = "Modelo para almacenar configurciones de maderas"

    name = fields.Char(string='Código', required=False, store=True, readonly=True)
    color_madera_id = fields.Many2one(comodel_name='product.template',
                                      string='Color pieza',
                                      required=True,
                                      domain="[('categ_base', '=', 'COLOR MADERA')]")
    cantos_id = fields.Many2one(comodel_name='product.template',
                                string='Chapa cantos',
                                required=True,
                                domain="[('categ_base', '=', 'CANTO')]")
    color_cantos_id = fields.Many2one(comodel_name='product.template',
                                      string='Color cantos',
                                      required=True,
                                      domain="[('categ_base', '=', 'COLOR MADERA')]")
    obsoleto = fields.Boolean(string='Obsoleto', required=False)

    @api.model
    def create(self, vals):
        res = super(WoodConfig, self).create(vals)
        used_keywords = []
        wood_config_ids = self.env['wood.config'].search([])
        keywords = sorted([''.join(i) for i in product(ascii_uppercase, repeat=3, )], reverse=True)

        new_string2compare = str(res.color_madera_id.id) + str(res.cantos_id.id) + str(res.color_cantos_id.id)
        print('New sting: ', new_string2compare)
        if new_string2compare == '273422732527342':
            res.update({'name': '000', })
        else:
            for record in wood_config_ids[:-1]:
                used_keywords.append(record.name)
                existing_string2compare = str(record.color_madera_id.id) + str(record.cantos_id.id) + \
                                          str(record.color_cantos_id.id)
                # print('Existing sting: ', existing_string2compare)
                if new_string2compare == existing_string2compare:
                    raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

            difference = list(set(keywords).difference(used_keywords))
            difference.sort(reverse=True)
            res.update({'name': difference[0], })
        return res

    def write(self, vals):
        used_keywords = []
        wood_config_ids = self.env['wood.config'].search([])
        c_madera = self.color_madera_id.id
        cantos = self.cantos_id.id
        c_cantos = self.color_cantos_id.id

        if vals.get('color_madera_id'):
            c_madera = vals.get('color_madera_id')
        elif vals.get('cantos_id'):
            cantos = vals.get('cantos_id')
        elif vals.get('color_cantos_id'):
            c_cantos = vals.get('color_cantos_id')

        new_string2compare = str(c_madera) + str(cantos) + str(c_cantos)
        for record in wood_config_ids[:-1]:
            used_keywords.append(record.name)
            existing_string2compare = str(record.color_madera_id.id) + str(record.cantos_id.id) + \
                                      str(record.color_cantos_id.id)
            if new_string2compare == existing_string2compare:
                raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

        return super(WoodConfig, self).write(vals)

    @api.depends('color_madera_id', 'cantos_id', 'color_cantos_id')
    def _compute_code_concat(self):
        for rec in self:
            rec.code_concat = str(rec.color_madera_id.default_code) + '-' + \
                              str(rec.cantos_id.default_code) + '-' + \
                              str(rec.color_cantos_id.default_code) or None
            rec.color_madera_name = str(rec.color_madera_id.name) or None
            rec.cantos_name = str(rec.cantos_id.name) or None
            rec.color_cantos_name = str(rec.color_cantos_id.name) or None
        return True

    code_concat = fields.Char(string='Códigos concatenados', required=False,
                              compute=_compute_code_concat, store=True)
    color_madera_name = fields.Char(string='Color pieza nombre', required=False,
                                    compute=_compute_code_concat, store=True)
    cantos_name = fields.Char(string='Chapa cantos nombre', required=False,
                                    compute=_compute_code_concat, store=True)
    color_cantos_name = fields.Char(string='Color cantos nombre', required=False,
                                    compute=_compute_code_concat, store=True)
