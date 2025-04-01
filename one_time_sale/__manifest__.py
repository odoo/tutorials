{
    'name': "One Time Sale",
    'version': '1.0',
    'depends': ['website_sale_subscription'],
    'author': "Odoo",
    'category': 'Sales/Subscriptions',
    'description': """
    This module enables the sale and purchase of subscription products with a one-time purchase option.
    """,
    'data': [
        'data/one_time_sale_tour.xml',
        'views/product_views.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'one_time_sale/static/src/**/*',
            ('remove', 'one_time_sale/static/src/js/tours/**')
        ],
        'web.assets_backend': [
            'one_time_sale/static/src/js/tours/**',
        ]
    },
    'license': 'OEEL-1'
}
