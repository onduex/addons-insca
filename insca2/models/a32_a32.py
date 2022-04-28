# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class A32A32(models.Model):
    _name = "a32.a32"
    _description = "Modelo para almacenar configurciones de a32"

    name = fields.Char(string='Código', required=False, store=True, readonly=True)
    color_metal1_id = fields.Many2one(comodel_name='product.template',
                                       string='Color MT1',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR METAL')]")
    color_metal2_id = fields.Many2one(comodel_name='product.template',
                                       string='Color MT2',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR METAL')]")
    color_metal3_id = fields.Many2one(comodel_name='product.template',
                                       string='Color MT3',
                                       required=True,
                                       domain="[('categ_base', '=', 'COLOR METAL')]")
    obsoleto = fields.Boolean(string='Obsoleto', required=False)

    @api.model
    def create(self, vals):
        res = super(A32A32, self).create(vals)
        used_keywords = []
        config_ids = self.env['a32.a32'].search([])
        keywords = sorted([''.join(i) for i in product(ascii_uppercase, repeat=3, )], reverse=True)

        new_string2compare = str(res.color_metal1_id.id) + str(res.color_metal2_id.id) + str(res.color_metal3_id.id)
        print('New sting: ', new_string2compare)

        for record in config_ids[:-1]:
            used_keywords.append(record.name)
            existing_string2compare = str(record.color_metal1_id.id) + str(record.color_metal2_id.id) + \
                                      str(record.color_metal3_id.id)
            print('Existing sting: ', existing_string2compare)
            if new_string2compare == existing_string2compare:
                raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

        difference = list(set(keywords).difference(used_keywords))
        difference.sort(reverse=True)
        res.update({'name': difference[0], })

        return res

    @api.depends('color_metal1_id', 'color_metal2_id', 'color_metal3_id')
    def _compute_code_concat(self):
        for rec in self:
            rec.code_concat = str(rec.color_metal1_id.default_code) + '-' + \
                              str(rec.color_metal2_id.default_code) + '-' + \
                              str(rec.color_metal3_id.default_code) or None
            rec.color_metal1_name = str(rec.color_metal1_id.name) or None
            rec.color_metal2_name = str(rec.color_metal2_id.name) or None
            rec.color_metal3_name = str(rec.color_metal3_id.name) or None
        return True

    code_concat = fields.Char(string='Códigos concatenados', required=False,
                              compute=_compute_code_concat, store=True)
    color_metal1_name = fields.Char(string='Color MT1 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
    color_metal2_name = fields.Char(string='Color MT2 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
    color_metal3_name = fields.Char(string='Color MT3 nombre', required=False,
                                     compute=_compute_code_concat, store=True)
