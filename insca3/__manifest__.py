# -*- coding: utf-8 -*-
{
    'name': "insca3",

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
        'base',
        'crm',
        'mrp',
    ],

    'external_dependencies': {
        'python': ['pysmb'],
    },

    # always loaded
    'data': [
        'data/res_groups_data.xml',
        'data/ir_actions_server.xml',
        'security/ir.model.access.csv',
        'views/folder_config.xml',
        'views/res_company_form.xml',
        'views/mrp_workorder_view.xml',
        'views/assets.xml',
        'wizards/print_bom_wiz.xml'
    ],

    'qweb': [
            'static/src/xml/check_ptg.xml',
        ],

    'installable': True,
    'application': True,
}
