# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'description': """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,

    'author': "Dimitris Mystriotis",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],

    'data': [],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/**/*',
        ],

    },
    'license': 'AGPL-3'
}
