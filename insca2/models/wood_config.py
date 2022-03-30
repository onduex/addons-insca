# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from itertools import product
from string import ascii_uppercase
from odoo.exceptions import ValidationError


class WoodConfig(models.Model):
    _name = "wood.config"
    _description = "Modelo para almacenar configurciones de maderas"

    name = fields.Char(string='Código', required=False, store=True, readonly=True)
    color_madera_id = fields.Many2one(comodel_name='product.template',
                                      string='Color madera',
                                      required=False,
                                      domain="[('categ_base', '=', 'COLOR MADERA')]")
    cantos_id = fields.Many2one(comodel_name='product.template',
                                string='Canto',
                                required=False,
                                domain="[('categ_base', '=', 'CANTO')]")

    @api.model
    def create(self, vals):
        res = super(WoodConfig, self).create(vals)
        wood_config_ids = self.env['wood.config'].search([])

        keywords = sorted([''.join(i) for i in product(ascii_uppercase, repeat=3, )], reverse=True)
        # print(keywords[res.id])
        res.update({'name': keywords[res.id],
                    })
        new_string2compare = str(res.color_madera_id.id) + str(res.cantos_id.id)
        print('New sting: ', new_string2compare)

        for record in wood_config_ids[:-1]:
            existing_string2compare = str(record.color_madera_id.id) + str(record.cantos_id.id)
            print('Existing sting: ', existing_string2compare)
            if new_string2compare == existing_string2compare:
                raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

        return res
