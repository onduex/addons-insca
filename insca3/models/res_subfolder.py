# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os
from itertools import product
from string import ascii_uppercase

from odoo import api, fields, models, _


class ResSubfolder(models.Model):
    _name = "res.subfolder"
    _description = "Modelo para almacenar las subcarpetas a crear"

    name = fields.Char(string='Descripción', required=True, store=True)
