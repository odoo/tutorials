# -*- coding: utf-8 -*-
{
    'name': "Awesome Dashboard",

    'summary': """
        Companion addon for the Odoo JS Framework Training
    """,

    'description': """
        Companion addon for the Odoo JS Framework Training
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail', 'crm'],

    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_dashboard/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
