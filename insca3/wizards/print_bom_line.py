# -*- coding: utf-8 -*-
# © 2023 Tomás Pascual (<tompascual@outlook.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class PrintBomLine(models.TransientModel):
    _name = 'print.bom.line'
    _description = 'BoM lines a imprimir'

    mrp_bom_line_level = fields.Char(string='Nivel', required=False)
    default_code = fields.Char(string='Referencia', required=False)
    name = fields.Char(string='Nombre', required=False)
    qty = fields.Float(string='Cantidad', required=False)
    has_bom_line_ids = fields.Integer(string='Tiene BoM', required=False)
    to_print = fields.Boolean(string='Imprimir', required=False)
