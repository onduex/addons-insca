# -*- coding: utf-8 -*-
{
    'name': "insca2",

    'summary': """
        Añadir tabla de configuración para la madera""",

    'description': """
        Añadir tabla de configuración para la madera""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': [
        'bi_sql_editor',
        'base',
        'stock',
        'mrp',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_packaging_wiz.xml',
        'views/product_inherit_views.xml',
        'views/wood_config.xml',
        'data/packaging_data.xml'
    ],

    'installable': True,
}
