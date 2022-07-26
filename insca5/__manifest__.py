# -*- coding: utf-8 -*-
{
    'name': "insca5",

    'summary': """
        Crear LdM para producto embalaje (EMB)""",

    'description': """
        Crear LdM para producto embalaje (EMB)""",

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
        'wizards/create_bom_wiz.xml',
        'views/product_inherit_views.xml',


    ],

    'installable': True,
}
