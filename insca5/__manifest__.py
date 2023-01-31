# -*- coding: utf-8 -*-
{
    'name': "insca5",

    'summary': """Crear productos desde ficha Categoría""",

    'description': """Crear productos desde ficha Categoría""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': [
        'product',
    ],

    # always loaded
    'data': [
        'views/category_inherit_views.xml',
        'wizards/create_product_wiz.xml'
    ],

    'installable': True,
    'application': False,
}
