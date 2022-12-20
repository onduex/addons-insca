from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResRotulacion(models.Model):
    _name = 'res.rotulacion'
    _description = 'Tabla de rotulación'

    type = fields.Selection(
        string='Tipo',
        selection=[('vin', 'Vinilo'), ('ser', 'Serigrafía'), ],
        required=False, )
    code = fields.Char(string='Código', required=False, default='/', readonly=True)
    name = fields.Char(string='Descripción', required=True)
    dimensions = fields.Char(string='Medidas', required=True)
    color = fields.Char(string='Colores', required=False)
    customer = fields.Char(string='Cliente', required=False)

    _sql_constraints = [
        ('res_rotulacion', 'UNIQUE (code)',
         _('El código debe ser único!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            varType = vals.get('type')
            if varType == 'vin':
                vals['code'] = self.env['ir.sequence'].next_by_code('insca2.vin.seq')
            elif varType == 'ser':
                vals['code'] = self.env['ir.sequence'].next_by_code('insca2.ser.seq')
            else:
                raise ValidationError(
                    _('Seleccione el tipo primero'))

        return super(ResRotulacion, self).create(vals_list)
