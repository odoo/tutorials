# -*- coding: utf-8 -*-
{
    'name': "Awesome Kanban",
    'summary': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban views"
    """,

    'description': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban views.
    """,

    'version': '0.1',
    'application': True,
    'category': 'Tutorials/AwesomeKanban',
    'installable': True,
    'depends': ['web', 'crm'],
    'demo': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_kanban/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
