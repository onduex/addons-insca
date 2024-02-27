# -*- coding: utf-8 -*-
{
    'name': "insca2",

    'summary': """
        Añadir tablas de configuraciónes""",

    'description': """
        Añadir tablas de configuraciónes""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'bi_sql_editor',
        'base',
        'stock',
        'mrp',
    ],

    # always loaded
    'data': [
        'wizards/create_packaging_wiz.xml',
        'views/product_inherit_views.xml',
        'views/wood_config.xml',
        'views/a80_a90_sequence.xml',
        'data/packaging_data.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
}
