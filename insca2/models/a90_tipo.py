from odoo import fields, models, api


class A90Type(models.Model):
    _name = 'a90.type'
    _description = 'Tipos para A90'

    name = fields.Char(string='Nombre', required=True)


class A90Thickness(models.Model):
    _name = 'a90.thickness'
    _description = 'Espesores para A90'

    name = fields.Float(string='Nombre', required=True)


class A90Density(models.Model):
    _name = 'a90.density'
    _description = 'Densidades para A90'

    name = fields.Float(string='Densidad (Kg/cm3)', required=False)
