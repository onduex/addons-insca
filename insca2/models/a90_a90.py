from odoo import fields, models, api, _


class A90A90(models.Model):
    _name = 'a90.a90'
    _description = 'Tabla de textil'

    name = fields.Char(string='Descripción', required=True)
    code = fields.Char(string='Código', required=False, default='/', readonly=True)

    _sql_constraints = [
        ('a90_a90', 'UNIQUE (code)',
         _('El código debe ser único!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', '/'):
                vals['code'] = self.env['ir.sequence'].next_by_code('insca2.a90.seq')
        return super(A90A90, self).create(vals_list)
