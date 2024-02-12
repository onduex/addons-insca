# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "insca5",
    'summary': """
        Módulo impresión report herrajes por orden de trabajo montaje""",

    'description': """
        Módulo impresión report herrajes por orden de trabajo montaje""",

    'version': '13.0',
    'author': 'Onduex sl',
    'website': 'http://www.onduex.com',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['mrp'
                ],

    "data": [
        'reports/external_layout_workorder.xml',
        'reports/external_layout_boxed_workorder.xml',
        'reports/declare.xml',
        'reports/report_herrajes.xml',
    ],

    "installable": True,
    "application": False,
}
