# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Awesome Owl",
    'category': 'Tutorials/AwesomeOwl',
    'version': '0.1',
    'author': "Odoo",
    'summary': """Starting module for "Discover the JS framework, chapter 1: Owl components" """,
    'description': """
        Starting module for "Discover the JS framework, chapter 1: Owl components"
    """,
    'depends': ['base', 'web'],
    'website': "https://www.odoo.com",
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
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
