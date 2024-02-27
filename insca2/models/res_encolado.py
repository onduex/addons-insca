from odoo import fields, models, api, _


class ResEncolado(models.Model):
    _name = 'res.encolado'
    _description = 'Parámetros encolado calculo de tiempos'
    _order = 'name asc'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True)
    value = fields.Float(string='Valor', required=False)
    unit = fields.Char(string='Unidades', required=True)
