from odoo import fields, models, api, _


class A80A80(models.Model):
    _name = 'a80.a80'
    _description = 'Tabla de cristal y metacrilato'

    name = fields.Char(string='Descripción', required=True)
    code = fields.Char(string='Código', required=False, default='/', readonly=True)
    tipo = fields.Selection(string='Tipo', selection=[('cristal', 'CRISTAL'),
                                                      ('metacrilato', 'METACRILATO')],
                            required=False, )
    espesor = fields.Selection(string='Espesor',
                               selection=[('1', '01mm'), ('2', '02mm'), ('3', '03mm'), ('4', '04mm'),
                                          ('5', '05mm'), ('6', '06mm'), ('7', '07mm'), ('8', '08mm'),
                                          ('9', '09mm'), ('10', '10mm'), ('11', '11mm'), ('12', '12mm'),
                                          ('13', '13mm'), ('14', '14mm'), ('15', '15mm'), ('16', '16mm'),
                                          ('17', '17mm'), ('18', '18mm'), ('19', '19mm'), ('20', '04mm'),
                                          ('21', '21mm'), ('22', '22mm'), ('23', '23mm'), ('24', '24mm'),
                                          ('25', '25mm'), ('26', '26mm'), ('27', '27mm'), ('28', '28mm'),
                                          ('29', '29mm'), ('30', '30mm'), ('31', '31mm'), ('32', '32mm'),
                                          ],
                               required=False, )

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
