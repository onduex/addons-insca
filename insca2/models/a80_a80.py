from odoo import fields, models, api, _


class A80A80(models.Model):
    _name = 'a80.a80'
    _description = 'Tabla de cristal y metacrilato'

    name = fields.Char(string='Descripción', required=True)
    code = fields.Char(string='Código', required=False, default='/', readonly=True)
    type = fields.Many2one(comodel_name='a80.type', string='Tipo', required=False)
    thikness = fields.Many2one(comodel_name='a80.thikness', string='Espesor', required=False)
    density = fields.Many2one(comodel_name='a80.density', string='Densidad', required=False)

    _sql_constraints = [
        ('a80_a80', 'UNIQUE (code)',
         _('El código debe ser único!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', '/'):
                vals['code'] = self.env['ir.sequence'].next_by_code('insca2.a80.seq')
        return super(A80A80, self).create(vals_list)
