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
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/supplier_list_views.xml',
        'views/assets.xml',
    ],

    'qweb': [
            'static/src/xml/check_sales.xml',
        ],



    'installable': True,
    'application': True,
}
