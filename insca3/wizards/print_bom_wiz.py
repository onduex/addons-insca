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

    bom_id = fields.Many2one(comodel_name='mrp.bom',
                             string="Lista de materiales",
                             readonly=False)

    bom_line_ids = fields.One2many(
        comodel_name='print.bom.line',
        inverse_name='id',
        string='Componente',
        required=False,
    )

    def print_all_bom_children_with_bom(self, ch, row, level):
        i, j = row, level
        j += 1
        line = (0, 0, {'to_print': True,
                       'mrp_bom_line_level': ("- - " * j) + ch.product_id.default_code,
                       'default_code': ch.product_id.default_code,
                       'name': ch.product_id.name,
                       'qty': ch.product_qty,
                       'has_bom_line_ids': len(ch.child_line_ids),
                       'route': ch.child_bom_id.vault_route or None,
                       'path': str(ch.product_id.png_link).
                replace('png', 'pdf').replace('0_PNG', '1_PDF') or None,
                       'parent_bom': ch.bom_id.product_tmpl_id.default_code or None,
                       })
        if line[2]['has_bom_line_ids'] != 0:
            lines.append(line)
        try:
            for child in ch.child_line_ids:
                i = self.print_all_bom_children_with_bom(child, i, j)

        except CacheMiss:
            # The Bom has no childs, thus it is the last level.
            # When a BoM has no childs, child_line_ids is None, this creates a
            # CacheMiss Error. However, this is expected because there really
            # cannot be child_line_ids.
            pass

        j -= 1
        return lines

    def get_all_bom_lines_with_bom(self):
        self.remove_bom_lines()
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

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

    def get_all_bom_lines_without_hrj(self):
        self.remove_bom_lines()
        lines_without_hrj = []
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

        for line in i:
            if line[2]['default_code'][0:4] == 'A70.':
                line[2]['to_print'] = False
                lines_without_hrj.append(line)
            else:
                lines_without_hrj.append(line)

        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines_without_hrj}

        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 2787,
            'target': 'new'}

    def get_all_bom_lines_only_mad(self):
        self.remove_bom_lines()
        lines_only_mad = []
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

        for line in i:
            if line[2]['default_code'][0:4] == 'A10.' or line[2]['default_code'][0:4] == 'A11.':
                line[2]['to_print'] = True
                lines_only_mad.append(line)
            else:
                line[2]['to_print'] = False
                lines_only_mad.append(line)

        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines_only_mad}

        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 2787,
            'target': 'new'}

    def get_all_bom_lines_only_ptg(self):
        self.remove_bom_lines()
        lines_only_ptg = []
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

        for line in i:
            if line[2]['route'] and 'PTG' not in line[2]['route']:
                line[2]['to_print'] = False
                lines_only_ptg.append(line)
            elif not line[2]['route']:
                line[2]['to_print'] = False
                lines_only_ptg.append(line)
            else:
                line[2]['to_print'] = True
                lines_only_ptg.append(line)

        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines_only_ptg}

        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 2787,
            'target': 'new'}

    def get_all_bom_lines_only_met(self):
        self.remove_bom_lines()
        lines_only_met = []
        lines_only_met2 = []
        lines_only_met_reactivate = []
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children_with_bom(ch, i, j)

        for line in i:
            if line[2]['parent_bom'][0:4] == 'A31.':
                line[2]['to_print'] = False
                lines_only_met.append(line)
            elif line[2]['parent_bom'][0:4] == 'A30.' and line[2]['default_code'][0:4] == 'A30.':
                line[2]['to_print'] = False
                lines_only_met.append(line)
            elif line[2]['default_code'][0:4] == 'A70.' \
                    or line[2]['default_code'][0:4] == 'A10.' \
                    or line[2]['default_code'][0:4] == 'A11.' \
                    or line[2]['default_code'][0:4] == 'A12.' \
                    or line[2]['default_code'][0:4] == 'A15.':
                line[2]['to_print'] = False
                lines_only_met.append(line)
            else:
                line[2]['to_print'] = True
                lines_only_met.append(line)

        for rec in lines_only_met:
            if rec[2]['to_print'] and \
                    (rec[2]['default_code'][0:4] == 'A30.' or rec[2]['default_code'][0:4] == 'A31.') and \
                    (rec[2]['parent_bom'][0:4] != 'A31.' or rec[2]['parent_bom'][0:4] != 'A32.'):
                lines_only_met_reactivate.append(rec[2]['parent_bom'])

        for line in lines_only_met:
            if line[2]['default_code'] in lines_only_met_reactivate:
                line[2]['to_print'] = True
                lines_only_met2.append(line)
            else:
                lines_only_met2.append(line)

        context = {'default_bom_id': self.bom_id.id,
                   'default_bom_line_ids': lines_only_met2}

        return {
            'name': 'Imprimir Lista de Materiales',
            'type': 'ir.actions.act_window',
            'res_model': 'print.bom.wiz',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 2787,
            'target': 'new'}

    def remove_bom_lines(self):
        lines.clear()
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

    # No se usa en el wizard
    def get_all_bom_lines(self):
        self.remove_bom_lines()
        i = 0
        for o in self.bom_id:
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_all_bom_children(ch, i, j)

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

    # No se usa en el wizard
    def print_all_bom_children(self, ch, row, level):
        i, j = row, level
        j += 1
        line = (0, 0, {'to_print': True,
                       'mrp_bom_line_level': ("- - " * j) + ch.product_id.default_code,
                       'default_code': ch.product_id.default_code,
                       'name': ch.product_id.name,
                       'qty': ch.product_qty,
                       'has_bom_line_ids': len(ch.child_line_ids),
                       })
        lines.append(line)
        try:
            for child in ch.child_line_ids:
                i = self.print_all_bom_children(child, i, j)

        except CacheMiss:
            # The Bom has no childs, thus it is the last level.
            # When a BoM has no childs, child_line_ids is None, this creates a
            # CacheMiss Error. However, this is expected because there really
            # cannot be child_line_ids.
            pass

        j -= 1
        return lines

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
