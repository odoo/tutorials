{
    'name': "One Time Sale",
    'version': '1.0',
    'depends': ['sale_subscription', 'website_sale_subscription'],
    'author': "Odoo",
    'category': 'Sales/Subscriptions',
    'description': """
    This module enables the sale and purchase of products with a one-time purchase option.
    """,
    'data': [
        'views/product_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'one_time_sale/static/src/**/*',
        ]
    },
    'license': 'LGPL-3'
}
