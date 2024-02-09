# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "insca5",
    'version': '13.0',
    'author': 'Onduex sl',
    'website': 'http://www.onduex.com',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['mrp',
                'mrp_workorder',
                ],

    "data": [
        # 'views/mrp_bom_view.xml',
        # 'views/mrp_production_menu.xml',
        # 'views/mrp_bom_component_view.xml',
        # 'views/product_template.xml',
        # 'views/hr_timesheet.xml',

        'reports/declare.xml',
        'reports/report_paperformat.xml',
        # 'reports/report_hoja_material3.xml',
        # 'reports/report_hoja_material2.xml',
        # 'reports/report_hoja_material.xml',
        # 'reports/report_hoja_compras.xml',
    ],

    "installable": True,
    "application": False,
}
