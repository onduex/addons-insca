from odoo import fields, models, api, _


class ResSeccionadora(models.Model):
    _name = 'res.seccionadora'
    _description = 'Parámetros seccionadora calculo de tiempos'
    _order = 'name asc'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True)
    value = fields.Integer(string='Valor', required=False)
    unit = fields.Char(string='Código', required=True)
