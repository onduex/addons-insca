from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    material = fields.Many2one(comodel_name="material", string="Material", required=False, store=True, tracking=1)
    acabado = fields.Many2one(comodel_name="acabado", string="Acabado", required=False, store=True, tracking=1)
    estado = fields.Selection(
        string='Estado',
        selection=[('lanzado', 'Lanzado'),
                   ('obsoleto', 'Obsoleto'), ],
        required=False,
        default='lanzado', tracking=1)
    name = fields.Char(tracking=1)
    default_code = fields.Char(tracking=1)
