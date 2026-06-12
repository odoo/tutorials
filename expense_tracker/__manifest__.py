{
    'name': "Expense Tracker",

    'author': "Odoo",
    'website': "https://www.odoo.com",

    'category': 'Tutorials',
    'version': '0.1',

    'depends': ['base', 'web'],
    'application': True,
    'installable': True,
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'expense_tracker.assets_expenses': [
            ('include', 'web._assets_helpers'),
            ('include', 'web._assets_backend_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            'web/static/lib/bootstrap/scss/_maps.scss',
            ('include', 'web._assets_bootstrap'),
            ('include', 'web._assets_core'),
            'web/static/src/libs/fontawesome/css/font-awesome.css',
            'expense_tracker/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
