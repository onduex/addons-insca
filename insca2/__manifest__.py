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
        'base'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/wood_config.xml',
    ],

    'installable': True,
}
