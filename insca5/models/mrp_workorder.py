# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from operator import itemgetter
from itertools import groupby

all_components = []
all_lines = []


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @staticmethod
    def recurse(lines, line_qty=1, count=0):
        for line in lines:
            count = count + 1
            all_components.append({'default_code': line['product_id']['default_code'],
                                   'name': line['product_id']['name'],
                                   'product_qty': line_qty * line.product_qty,
                                   'bom_id': line['bom_id']['product_tmpl_id']['default_code']
                                   })
            if len(line.child_line_ids) > 0:
                MrpWorkorder.recurse(line.child_line_ids, line_qty=line_qty * line.product_qty)

    @staticmethod
    def compute_all_lines():
        components = []
        all_components.sort(key=itemgetter('name'))
        for component in all_components:
            if component['default_code'][0:3] == 'A70':
                components.append({'default_code': component['default_code'],
                                   'name': component['name'],
                                   'product_qty': component['product_qty'],
                                   'bom_id': component['bom_id']
                                   })
        return components

    def compute_all_lines_and_sum(self):
        components = []
        key_list = []
        value_list = []
        all_components_sum = []
        all_components_sum_by_section = []

        for component in all_components:
            unique_code = str(component['default_code']) + str(component['bom_id'])
            components.append({'default_code': component['default_code'],
                               'name': component['name'],
                               'product_qty': component['product_qty'] * self.qty_production,
                               'bom_id': component['bom_id'],
                               'unique_code': unique_code,
                               })
        all_components.clear()
        all_components_sum.clear()
        all_components_sum_by_section.clear()
        for component in components:
            if component['default_code'][0:3] == 'A70':
                unique_code = str(component['default_code']) + str(component['bom_id'])
                if unique_code not in [x['unique_code'] for x in all_components_sum]:
                    all_components_sum.append({'default_code': component['default_code'],
                                               'name': component['name'],
                                               'product_qty': component['product_qty'],
                                               'bom_id': component['bom_id'],
                                               'unique_code': unique_code,
                                               })
                else:
                    for component_sum in all_components_sum:
                        if component_sum['unique_code'] == component['unique_code']:
                            component_sum['product_qty'] += component['product_qty']
        all_components_sum_by_section = sorted(all_components_sum, key=itemgetter('bom_id'))
        for key, value in groupby(all_components_sum_by_section, key=itemgetter('bom_id')):
            key_list.append(key)
            value_list.append(list(value))

        for i in value_list:
            i.sort(key=lambda x: x['default_code'])

        return key_list, value_list
