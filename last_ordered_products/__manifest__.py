{
    'name': "Last Ordered Products",
    'version': '1.0',
    'depends': ['product'],
    'author': "Parthav Chodvadiya (PPCH)",
    'category': '',
    'description': """
    Show last ordered products for customers in sale order and for vendors in purchase order
    """,
    'data': [
        'views/product_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'last_ordered_products/static/src/**/*.js',
            'last_ordered_products/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}
