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
                                      domain="[('categ_base', '=', [('COLOR MADERA'), ('COLOR METAL'), ('MADERA')])]"
                                      )
    color_metal2_id = fields.Many2one(comodel_name='product.template',
                                      string='Color MT2',
                                      required=True,
                                      domain="[('categ_base', '=', [('COLOR MADERA'), ('COLOR METAL'), ('MADERA')])]"
                                      )
    color_metal3_id = fields.Many2one(comodel_name='product.template',
                                      string='Color MT3',
                                      required=True,
                                      domain="[('categ_base', '=', [('COLOR MADERA'), ('COLOR METAL'), ('MADERA')])]"
                                      )
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

    def write(self, vals):
        used_keywords = []
        config_ids = self.env['a32.a32'].search([])
        c_metal1 = self.color_metal1_id.id
        c_metal2 = self.color_metal2_id.id
        c_metal3 = self.color_metal3_id.id

        if vals.get('color_metal1_id'):
            c_metal1 = vals.get('color_metal1_id')
        elif vals.get('color_metal2_id'):
            c_metal2 = vals.get('color_metal2_id')
        elif vals.get('color_metal3_id'):
            c_metal3 = vals.get('color_metal3_id')

        new_string2compare = str(c_metal1) + str(c_metal2) + str(c_metal3)
        print('New sting: ', new_string2compare)
        for record in config_ids[:-1]:
            used_keywords.append(record.name)
            existing_string2compare = str(record.color_metal1_id.id) + str(record.color_metal2_id.id) + \
                                      str(record.color_metal3_id.id)
            print('Existing sting: ', existing_string2compare)
            if new_string2compare == existing_string2compare:
                raise ValidationError(_('La nueva combinación existe con el código %s' % record.name))

        return super(A32A32, self).write(vals)

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
