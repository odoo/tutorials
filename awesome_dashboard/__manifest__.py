# -*- coding: utf-8 -*-
{
    'name': "Awesome Dashboard",

    'summary': """
<<<<<<< HEAD
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,

    'description': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
=======
        Companion addon for the Odoo JS Framework Training
    """,

    'description': """
        Companion addon for the Odoo JS Framework Training
>>>>>>> 7064949f3 ([ADD] Discover the JavaScript framework)
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
            ('remove', 'awesome_dashboard/static/src/dashboard/**/*'),
        ],
        'awesome_dashboard.dashboard': [
            'awesome_dashboard/static/src/dashboard/**/*'
        ]

    },
    'license': 'AGPL-3'
}
