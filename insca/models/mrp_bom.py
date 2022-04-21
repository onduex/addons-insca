# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    vault_route = fields.Char(related='product_tmpl_id.vault_route', string='Vault Ruta', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        product_id = vals_list[0]['product_tmpl_id']
        product_for_bom = self.env['product.template'].search([('id', '=', product_id)])
        mrp_routing = self.env['mrp.routing'].search([('name', '=', product_for_bom.vault_route)])

        for bom in res:
            res_code = self.env['res.code'].search([('name', '=', bom.product_tmpl_id.vault_code)])
            if res_code.type_mrp:
                res.update({'type': res_code.type_mrp})

            if product_for_bom.vault_route and not len(mrp_routing):
                raise ValidationError(_('La ruta %s del producto %s no existe en Odoo'
                                        % (bom.product_tmpl_id.vault_route, bom.product_tmpl_id.name)))
            elif product_for_bom.vault_route and len(mrp_routing):
                res.update({'routing_id': mrp_routing.id})
        return res

    def write(self, vals_list):
        lines = []
        product_ids = []

        if self.product_tmpl_id.vault_code == 'A31P' and self.is_vault_bom:

            product_ids += self.env['product.product'].\
                search([('inventor_color', '=', self.product_tmpl_id.vault_color)])
            product_ids += self.env['product.product'].\
                search([('default_code', '=', self.product_tmpl_id.default_code[:-3] + '000')])
            for product in product_ids:
                lines.append((0, 0, {'product_id': product.id, 'product_qty': 1}))
            vals_list.update({'bom_line_ids': lines})
        return super(MrpBom, self).write(vals_list)


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record in res:
            # Código A31 borrar líneas de BoM
            if record.bom_id.product_tmpl_id.vault_code == 'A31P' and \
                    record.bom_id.is_vault_bom and \
                    record.product_tmpl_id.vault_code == 'A30':
                print('Delete %s of %s' % (record.display_name, record.bom_id.product_tmpl_id.default_code))
                record.unlink()
        return res
