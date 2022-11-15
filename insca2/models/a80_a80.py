from odoo import fields, models, api, _


class A80A80(models.Model):
    _name = 'a80.a80'
    _description = 'Tabla de cristal y metacrilato'

    name = fields.Char(string='Descripción', required=True)
    code = fields.Char(string='Código', required=False, default='/', readonly=True)

    type = fields.Many2one(comodel_name='a80.type', string='Type', required=False)
    density = fields.Many2one(comodel_name='a80.density', string='Density', required=False)
    thickness = fields.Many2one(comodel_name='a80.thickness', string='Thickness', required=False)

    tipo = fields.Char(string='Tipo', required=False, compute='onchange_for_char')
    densidad = fields.Char(string='Densidad', required=False, compute='onchange_for_char')
    espesor = fields.Char(string='Espesor', required=False, compute='onchange_for_char')

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

    @api.depends('type', 'thickness', 'density')
    def onchange_for_char(self):
        for rec in self:
            rec.tipo = rec.type.name
            rec.espesor = rec.thickness.name
            rec.densidad = rec.density.name
        return True
