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
        'product',
        'stock',
        'mrp',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_inherit_views.xml',
        'views/product_data.xml',
        'views/mrp_bom_inherit_views.xml',

    ],

    'installable': True,
}
