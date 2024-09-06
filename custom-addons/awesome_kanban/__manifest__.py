# -*- coding: utf-8 -*-
{
    'name': "Awesome Kanban",
    'summary': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban view"
    """,

    'description': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban view.
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
            'static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
