# -*- coding: utf-8 -*-
{
    'name': "Awesome Owl",
    'summary': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,
    'description': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com",
    'category': 'Tutorials/AwesomeOwl',
    'version': '0.1',
    'depends': ['base', 'web'],
    'application': True,
    'installable': True,
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'awesome_owl.assets_playground': [
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            'web/static/lib/bootstrap/scss/_maps.scss',
            ('include', 'web._assets_bootstrap'),
            ('include', 'web._assets_core'),
            'web/static/src/libs/fontawesome/css/font-awesome.css',
            'awesome_owl/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
