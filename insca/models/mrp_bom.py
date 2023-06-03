# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.model_create_multi
    def create(self, vals_list):
        # Borrado de las mrp.bom.lines que vienen de vault
        product_ids = []
        lines = []
        new_line_list = []
        res = super().create(vals_list)
        for record in res:

            # Código A11 update lines that rainbow has removed
            if record.bom_id.product_tmpl_id.vault_code == 'A11' and \
                    record.bom_id.is_vault_bom:
                qty = ''
                # Obtener las nuevas líneas a crear
                if record.bom_id.product_tmpl_id.vault_color:
                    product = self.env['product.product']. \
                        search([('default_code', '=', record.bom_id.product_tmpl_id.vault_color),
                                ('default_code', '!=', 'I0039Y')])
                    if product.categ_base == 'COLOR MADERA':
                        qty = str(record.bom_id.product_tmpl_id.vault_sup_pintada)
                        lines.append((0, 0, {'bom_id': record.bom_id, 'product_id': product.id, 'product_qty': qty}))
                if record.bom_id.product_tmpl_id.vault_edge_pin_code:
                    product = self.env['product.product']. \
                        search([('default_code', '=', record.bom_id.product_tmpl_id.vault_edge_pin_code),
                                ('default_code', '!=', 'I0039Y')])
                    if product.categ_base == 'COLOR MADERA':
                        qty = str(record.bom_id.product_tmpl_id.vault_edge_painted_sup)
                        lines.append((0, 0, {'bom_id': record.bom_id, 'product_id': product.id, 'product_qty': qty}))
                if record.bom_id.product_tmpl_id.vault_edge_code:
                    product = self.env['product.product']. \
                        search([('default_code', '=', record.bom_id.product_tmpl_id.vault_edge_code),
                                ('default_code', '!=', '000000')])
                    if product.categ_base == 'CANTO':
                        qty = str(record.bom_id.product_tmpl_id.vault_edge_len)
                        lines.append((0, 0, {'bom_id': record.bom_id, 'product_id': product.id, 'product_qty': qty}))
                for rec in lines:
                    new_bom_lines_id = self.env['mrp.bom.line'].search([('bom_id', '=', rec[2]['bom_id'].id),
                                                                        ('product_id', '=', rec[2]['product_id'])])
                    if not new_bom_lines_id:
                        self.env['mrp.bom.line'].sudo().create({'bom_id': rec[2]['bom_id'].id,
                                                                'product_id': rec[2]['product_id'],
                                                                'product_qty': rec[2]['product_qty']})

            # Código A31 borrar líneas de BoM
            if record.bom_id.product_tmpl_id.vault_code == 'A31P' and \
                    record.bom_id.product_tmpl_id.default_code[-3:] != '000' and \
                    record.bom_id.is_vault_bom and \
                    record.product_tmpl_id.vault_code == 'A30':
                # Obtener las nuevas líneas a crear
                product_ids_max = self.env['product.product']. \
                    search([('default_code', '=', record.bom_id.product_tmpl_id.default_code[:-3] + '000')])
                if record.bom_id.product_tmpl_id.vault_color:
                    product_ids += self.env['product.product']. \
                        search([('default_code', '=', record.bom_id.product_tmpl_id.vault_color)])
                product_ids += max(product_ids_max)
                for product in product_ids:
                    lines.append((0, 0, {'bom_id': record.bom_id, 'product_id': product.id, 'product_qty': 1}))
                # print('Delete %s of %s' % (record.display_name, record.bom_id.product_tmpl_id.default_code))
                record.unlink()
            for rec in lines:
                new_bom_lines_id = self.env['mrp.bom.line'].search([('bom_id', '=', rec[2]['bom_id'].id),
                                                                    ('product_id', '=', rec[2]['product_id'])])
                if not new_bom_lines_id:
                    self.env['mrp.bom.line'].sudo().create({'bom_id': rec[2]['bom_id'].id,
                                                            'product_id': rec[2]['product_id'],
                                                            'product_qty': 1})

        return res

    def write(self, values):
        res = super().write(values)
        # Código A10
        if self.product_id.code[0:3] == 'A10':
            qty = ''
            lines = []
            if self.product_id.vault_material_code:
                product = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_material_code)])
                qty = self.product_id.vault_sup_madera
                if product:
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            if self.product_id.vault_edge_code:
                product = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_edge_code),
                            ('default_code', '!=', '000000')])
                qty = self.product_id.vault_edge_len
                if product:
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            if self.product_id.vault_color:
                if self.product_id.vault_sup_pintada != 0.0:
                    product = self.env['product.product']. \
                        search([('default_code', '=', self.product_id.vault_color),
                                ('default_code', '!=', 'I0039Y')])
                    qty = self.product_id.vault_sup_pintada
                    if product:
                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            if self.product_id.vault_edge_pin_code:
                if self.product_id.vault_edge_painted_sup != 0.0:
                    product = self.env['product.product']. \
                        search([('default_code', '=', self.product_id.vault_edge_pin_code),
                                ('default_code', '!=', 'I0039Y')])
                    qty = self.product_id.vault_edge_painted_sup
                    if product:
                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            if len(lines) > 0:
                self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código A30
        elif self.product_id.code[0:3] == 'A30' and self.product_id.default_code[-3:] == '000':
            lines = []
            product_ids = []
            if self.product_id.vault_material_code:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_material_code)])
            for product in product_ids:
                if self.product_id.name:
                    qty = 0.0001
                    if self.product_id.name[0:3] == 'CPF' or self.product_id.name[0:3] == 'CPC':
                        qty = self.product_id.vault_sup_madera
                    if self.product_id.name[0:2] == 'TR' or \
                            self.product_id.name[0:2] == 'TC' or \
                            self.product_id.name[0:2] == 'TO' or \
                            self.product_id.name[0:2] == 'MZ' and float(self.product_id.vault_length_tub) != 0.0:
                        if float(self.product_id.vault_length_tub) != 0.0:
                            qty = float(self.product_id.vault_length_tub) / 1000
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código A30P
        elif self.product_id.code[0:3] == 'A30' and self.product_id.default_code[-3:] != '000':
            qty = ''
            lines = []
            product_ids = []
            product_ids_max = self.env['product.product']. \
                search([('default_code', '=', self.product_id.default_code[:-3] + '000')])
            if self.product_id.vault_color:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_color)])
            product_ids += max(product_ids_max)
            for product in product_ids:
                if product.categ_base == 'COLOR METAL':
                    if float(self.product_id.vault_sup_pintada) != 0.0:
                        qty = str(float(self.product_id.vault_sup_pintada))
                else:
                    qty = 1
                lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                qty = None
            self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código A50
        elif self.product_id.code[0:3] == 'A50':
            lines = []
            product_ids = []
            if self.product_id.vault_purchase_code:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_purchase_code)])
            for product in product_ids:
                if self.product_id.vault_length_cut:
                    qty = self.product_id.vault_length_cut
                else:
                    qty = 1
                lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                qty = None
            self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código A70
        elif self.product_id.code[0:3] == 'A70':
            lines = []
            product_ids = []
            if self.product_id.vault_purchase_code:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_purchase_code)])
            if self.product_id.vault_left_hand:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_left_hand)])
            if self.product_id.vault_right_hand:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_right_hand)])
            for product in product_ids:
                qty = 0.0
                if self.product_id.vault_length_tub:
                    if self.product_id.vault_length_tub is not None:
                        qty = float(self.product_id.vault_length_tub) / 1000
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                else:
                    qty = 1
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
            self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código A90
        elif self.product_id.code[0:3] == 'A90':
            lines = []
            product_ids = []
            if self.product_id.vault_purchase_code:
                product_ids = self.env['product.product']. \
                    search([('default_code', '=', self.product_id.vault_purchase_code)])
            for product in product_ids:
                if self.product_id.vault_sup_madera:
                    qty = self.product_id.vault_sup_madera
                else:
                    qty = 1
                lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                qty = None
            self.child_bom_id.sudo().update({'bom_line_ids': lines})
        # Código EM0
        elif self.product_id.code[0:3] == 'EM0':
            lines = []
            product_ids = self.env['product.product']. \
                search([('default_code', 'ilike', self.product_id.default_code[4:]),
                        ('is_old_revision', '=', False)])
            if product_ids:
                for product in product_ids:
                    if product['name'][:5] == 'BULTO':
                        qty = product.product_package_number
                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                self.child_bom_id.sudo().update({'bom_line_ids': lines})
        return res


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    vault_route = fields.Char(related='product_tmpl_id.vault_route', string='Vault Ruta', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        product_id = vals_list[0]['product_tmpl_id']
        product_for_bom = self.env['product.template'].search([('id', '=', product_id)])
        mrp_routing = self.env['mrp.routing'].search([('name', '=', product_for_bom.vault_route)])
        product_ids = []
        lines = []

        for bom in res:
            res_code = self.env['res.code'].search([('name', '=', bom.product_tmpl_id.vault_code)])

            if res_code.type_mrp:
                res.update({'type': res_code.type_mrp})
                if res_code.type_mrp == 'subcontract':
                    res.update({'subcontractor_ids': [(6, 0, [x.id for x in res_code.supplier_ids])],
                                'location_id': 45,  # INSCA TRADEMARK, S.L.: Subcontracting Location
                                'product_id': product_for_bom.product_variant_id.id,
                                })

            if product_for_bom.vault_route and not len(mrp_routing):
                raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                        % (bom.product_tmpl_id.vault_route, bom.product_tmpl_id.name)))
            elif product_for_bom.vault_route and len(mrp_routing):
                res.update({'routing_id': mrp_routing.id})

            # add extra lines to A31P codes
            if bom.product_tmpl_id.vault_code == 'A31P' and \
                    bom.product_tmpl_id.default_code[-3:] != '000' and \
                    bom.is_vault_bom:
                product_ids_max = self.env['product.product']. \
                    search([('default_code', '=', bom.product_tmpl_id.default_code[:-3] + '000')])
                if bom.product_tmpl_id.vault_color:
                    product_ids += self.env['product.product']. \
                        search([('default_code', '=', bom.product_tmpl_id.vault_color)])
                product_ids += max(product_ids_max)
                for product in product_ids:
                    if product.categ_base == 'COLOR METAL':
                        qty = str(bom.product_tmpl_id.vault_sup_pintada)
                    else:
                        qty = 1
                    lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                    qty = None
                if bom.product_tmpl_id.active is True:
                    res.update({'bom_line_ids': lines})
                if bom.product_tmpl_id.active is False and bom.is_old_revision is True:
                    bom.sudo().write({'active': False})

            # add extra lines to A11 codes
            if bom.product_tmpl_id.vault_code == 'A11' and bom.is_vault_bom:
                qty = ''
                if bom.product_tmpl_id.vault_color:
                    if bom.product_tmpl_id.vault_sup_pintada:
                        product = self.env['product.product']. \
                            search([('default_code', '=', bom.product_tmpl_id.vault_color),
                                    ('default_code', '!=', 'I0039Y')])
                        if product.categ_base == 'COLOR MADERA':
                            if bom.product_tmpl_id.vault_sup_pintada:
                                qty = str(bom.product_tmpl_id.vault_sup_pintada)
                        if product:
                            lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                if bom.product_tmpl_id.vault_edge_code:
                    product = self.env['product.product']. \
                        search([('default_code', '=', bom.product_tmpl_id.vault_edge_code),
                                ('default_code', '!=', '000000')])
                    if product.categ_base == 'CANTO':
                        if bom.product_tmpl_id.vault_edge_len:
                            qty = bom.product_tmpl_id.vault_edge_len
                    if product:
                        lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                if bom.product_tmpl_id.vault_edge_pin_code:
                    if bom.product_tmpl_id.vault_edge_painted_sup:
                        product = self.env['product.product']. \
                            search([('default_code', '=', bom.product_tmpl_id.vault_edge_pin_code),
                                    ('default_code', '!=', 'I0039Y')])
                        if product.categ_base == 'COLOR MADERA':
                            if bom.product_tmpl_id.vault_edge_painted_sup:
                                qty = str(bom.product_tmpl_id.vault_edge_painted_sup)
                        if product:
                            lines.append((0, 0, {'product_id': product.id, 'product_qty': qty}))
                if bom.product_tmpl_id.active is True:
                    res.update({'bom_line_ids': lines})
                if bom.product_tmpl_id.active is False and bom.is_old_revision is True:
                    bom.sudo().write({'active': False})
        return res
