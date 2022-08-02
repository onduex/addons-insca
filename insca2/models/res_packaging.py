from odoo import fields, models, api, _


class ResPackaging(models.Model):
    _name = 'res.packaging'
    _description = 'Valores por defecto par el cálculo de embalajes'

    name = fields.Char(string='Nombre', required=False)
    code = fields.Char(string='Código', required=False)
    value = fields.Integer(string='Valor', required=False)

