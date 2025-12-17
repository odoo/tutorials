{
    'author': 'Odoo S.A.',
    'name': 'Deposit Rental App',
    'description': """
    Implements a security deposit feature in the Rental app
    to manage refundable deposits for rental products.
    """,
    'depends': ['sale_renting', 'website_sale'],
    'license': 'LGPL-3',
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/template_views.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'deposit_rental/static/src/deposit_amount.js',
        ],
    },
    'application': True,
    'installable': True
}
