# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TipoPieza(models.Model):
    _name = "tipo.pieza"
    _description = "Modelo para almacenar los tipos de pieza"

    name = fields.Char(string='Descripción', required=False, store=True)
    abreviatura = fields.Char(string='Abreviatura', required=False)
