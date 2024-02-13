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
            all_components.append({'product_qty': line_qty * line.product_qty,
                                   'default_code': line['product_id']['default_code'],
                                   'name': line['product_id']['name'],
                                   'bom_id': line['bom_id']['id']
                                   })
            if len(line.child_line_ids) > 0:
                MrpWorkorder.recurse(line.child_line_ids, line_qty=line_qty * line.product_qty)

    @staticmethod
    def compute_all_lines():
        components = []
        all_components.sort(key=itemgetter('name'))
        for component in all_components:
            if component['default_code'][0:3] == 'A70':
                components.append({'product_qty': component['product_qty'],
                                   'default_code': component['default_code'],
                                   'name': component['name'],
                                   'bom_id': component['bom_id']
                                   })
        all_components.clear()
        return components
