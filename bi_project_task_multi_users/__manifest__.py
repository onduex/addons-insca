# -- coding: utf-8 --
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Assign Multiple Users to Project Task',
    'version': '13.0.0.0',
    'category': 'Project',
    'summary': 'Project Tasks Multi Users Assignee on project task assignee to multi users on task multiple user Assignee for project tasks Multi Users Assignee on task multiple user Assignee for tasks assign task to multi user assign task to multiple users task assign',
    'description': """ 

        Assign Multiple Users For Project task in odoo,
        Allowed Multi Users for Single Task,
        Task Visible to Assigned Users in odoo,
        Assign Multi Users to Task in odoo,
        Visible Task to Allowed Users in odoo,
        Multiple Users For Project task in odoo,
    
    """,
    'author': 'BrowseInfo',
    "price": 15,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'security/multi_user_assign_security.xml',
        'views/project_task_view.xml',

    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/6aVynXL5OkQ',
    "images":['static/description/Banner.png'],
}
