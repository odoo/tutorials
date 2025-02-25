# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Awesome Owl",
    'summary': "Learning the Owl framework",
    'description': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,
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
