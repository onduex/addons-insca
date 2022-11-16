from odoo import fields, models, api, _


class A90A90(models.Model):
    _name = 'a90.a90'
    _description = 'Tabla de textil'

    name = fields.Char(string='Descripción', required=True)
    code = fields.Char(string='Código', required=False, default='/', readonly=True)

    type = fields.Many2one(comodel_name='a90.type', string='Type', required=False)
    density = fields.Many2one(comodel_name='a90.density', string='Density', required=False)
    thickness = fields.Many2one(comodel_name='a90.thickness', string='Thickness', required=False)

    tipo = fields.Char(string='Tipo', required=False, compute='onchange_for_char')
    densidad = fields.Char(string='Densidad', required=False, compute='onchange_for_char')
    espesor = fields.Char(string='Espesor', required=False, compute='onchange_for_char')

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

    @api.depends('thickness')
    def onchange_for_char(self):
        for rec in self:
            rec.tipo = rec.type.name
            rec.espesor = rec.thickness.name
            rec.densidad = rec.density.name
        return True
