from odoo import fields, models, api, _


class ResChapadora(models.Model):
    _name = 'res.chapadora'
    _description = 'Parámetros chapadora calculo de tiempos'
    _order = 'name asc'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True)
    value = fields.Float(string='Valor', required=False)
    unit = fields.Char(string='Unidades', required=True)
