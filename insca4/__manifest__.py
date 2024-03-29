# -*- coding: utf-8 -*-
{
    'name': "insca4",

    'summary': """LdM para proveedores""",

    'description': """LdM para proveedores""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',
        'purchase',
        'utm',
        'web_tree_dynamic_colored_field'
    ],

    # always loaded
    'data': [
        'data/res_groups_data.xml',
        'security/ir.model.access.csv',
        'views/supplier_list_views.xml',
        'views/assets.xml',
        'reports/etiquetas.xml',
        'reports/declare_reports.xml',

    ],

    'qweb': [
            'static/src/xml/check_sales.xml',
        ],



    'installable': True,
    'application': True,
}
