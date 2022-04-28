# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class A12A15(models.Model):
    _name = "a12.a15"
    _description = "Modelo para almacenar configurciones de a12 y a15"

    name = fields.Char(string='Código', required=False, store=True, readonly=True)
    color_madera1_id = fields.Many2one(comodel_name='product.template',
                                       string='Color M1',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR MADERA')]")
    color_madera2_id = fields.Many2one(comodel_name='product.template',
                                       string='Color M2',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR MADERA')]")
    color_madera3_id = fields.Many2one(comodel_name='product.template',
                                       string='Color M3',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR MADERA')]")
    obsoleto = fields.Boolean(string='Obsoleto', required=False)

    @api.model
    def create(self, vals):
        res = super(A12A15, self).create(vals)
        used_keywords = []
        config_ids = self.env['a12.a15'].search([])
        keywords = sorted([''.join(i) for i in product(ascii_uppercase, repeat=3, )], reverse=True)

        new_string2compare = str(res.color_madera1_id.id) + str(res.color_madera2_id.id) + str(res.color_madera3_id.id)
        print('New sting: ', new_string2compare)

        for record in config_ids[:-1]:
            used_keywords.append(record.name)
            existing_string2compare = str(record.color_madera1_id.id) + str(record.color_madera2_id.id) + \
                                      str(record.color_madera3_id.id)
            print('Existing sting: ', existing_string2compare)
            if new_string2compare == existing_string2compare:
                raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

        difference = list(set(keywords).difference(used_keywords))
        difference.sort(reverse=True)
        res.update({'name': difference[0], })

        return res

    @api.depends('color_madera1_id', 'color_madera3_id', 'color_madera3_id')
    def _compute_code_concat(self):
        for rec in self:
            rec.code_concat = str(rec.color_madera1_id.default_code) + '-' + \
                              str(rec.color_madera2_id.default_code) + '-' + \
                              str(rec.color_madera3_id.default_code) or None
            rec.color_madera1_name = str(rec.color_madera1_id.name) or None
            rec.color_madera2_name = str(rec.color_madera2_id.name) or None
            rec.color_madera3_name = str(rec.color_madera3_id.name) or None
        return True

    code_concat = fields.Char(string='Códigos concatenados', required=False,
                              compute=_compute_code_concat, store=True)
    color_madera1_name = fields.Char(string='Color M1 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
    color_madera2_name = fields.Char(string='Color M2 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
    color_madera3_name = fields.Char(string='Color M3 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
