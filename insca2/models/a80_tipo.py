from odoo import fields, models, api


class A80Type(models.Model):
    _name = 'a80.type'
    _description = 'Tipos para A80'

    name = fields.Char(string='Nombre', required=True)


class A80Thickness(models.Model):
    _name = 'a80.thickness'
    _description = 'Espesores para A80'

    name = fields.Float(string='Nombre', required=True)


class A80Density(models.Model):
    _name = 'a80.density'
    _description = 'Densidades para A80'

    name = fields.Float(string='Densidad (Kg/cm3)', required=False)


class A80Finished(models.Model):
    _name = 'a80.finished'
    _description = 'Acabados para A80'

    name = fields.Char(string='Acabado', required=False)
