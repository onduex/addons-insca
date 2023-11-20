# -*- coding: utf-8 -*-
# © 2023 Tomás Pascual (<tompascual@outlook.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import CacheMiss
import pprint
pp = pprint.PrettyPrinter(indent=4)
lines = []


class PrintBomWiz(models.TransientModel):
    _name = 'print.bom.wiz'
    _description = 'Wizard para imprimir LdM'

    def print_bom_children(self, ch, row, level):
        i, j = row, level
        j += 1
        line = (0, 0, {'mrp_bom_line_level': ("- - " * j) + ch.product_id.default_code,
                       'default_code': ch.product_id.default_code,
                       'name': ch.product_id.name,
                       'qty': ch.product_qty,
                       })
        # print(("> " * j), ch.product_id.default_code)
        # print(line)
        lines.append(line)
        try:
            for child in ch.child_line_ids:
                i = self.print_bom_children(child, i, j)

        except CacheMiss:
            # The Bom has no childs, thus it is the last level.
            # When a BoM has no childs, child_line_ids is None, this creates a
            # CacheMiss Error. However, this is expected because there really
            # cannot be child_line_ids.
            pass

        j -= 1
        return lines

    def get_bom_lines(self):
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_bom_children(ch, i, j)
        pp.pprint(lines)

        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines}
        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 2787,
            'target': 'new'}

    bom_id = fields.Many2one(comodel_name='mrp.bom',
                             string="Lista de materiales",
                             ondelete='cascade',
                             readonly=False)

    bom_line_ids = fields.One2many(
        comodel_name='print.bom.line',
        inverse_name='id',
        string='Componente',
        required=False,
        )

    @api.model
    def print_bom(self):
        context = {'default_bom_id': self.bom_id.id}
        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            # 'context': self.env.context,
            'res_id': 842,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new'}
