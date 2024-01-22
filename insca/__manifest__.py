# -*- coding: utf-8 -*-
{
    'name': "insca",

    'summary': """
        Modificación de vistas y algunos métodos""",

    'description': """
        Modificación de vistas y algunos métodos""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': [
        'rainbow_bom_structure',
        'product',
        'stock',
        'mrp',
        'mrp_production_parent',
        'mrp_bom_open_png',

    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_inherit_views.xml',
        'views/product_data.xml',
        'views/mrp_bom_inherit_views.xml',
        'views/mrp_workorder_inherit_views.xml',
        'data/ir_actions_server.xml',
    ],

    'installable': True,
}
