from odoo import fields, models, api, _


class ResPintura(models.Model):
    _name = 'res.pintura'
    _description = 'Parámetros pintura calculo de tiempos'
    _order = 'name asc'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True)
    value = fields.Integer(string='Valor', required=False)
    unit = fields.Char(string='Código', required=True)
