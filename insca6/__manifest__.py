# -*- coding: utf-8 -*-
{
    'name': "insca6",

    'summary': """
        Módulo expedientes""",

    'description': """
        Módulo expedientes""",

    'author': "Onduex sl",
    'website': "http://www.onduex.com",

    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': ['pysmb'],
    },

    # always loaded
    'data': [
        'data/res_groups_data.xml',
        'security/ir.model.access.csv',
        'views/folder_config.xml',
        'views/res_company_form.xml',
    ],

    'installable': True,
    'application': True,
}
