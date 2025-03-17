{
    'name': "Last Ordered Products",
    'version': '1.0',
    'depends': ['sale_management', 'purchase', 'stock'],
    'author': "Parthav Chodvadiya (PPCH)",
    'category': '',
    'description': """
    Show last ordered products for customers in sale order and for vendors in purchase order
    """,
    'data': [
        'views/account_move_form.xml',
        'views/sale_order_form.xml',
        'views/purchase_order_form.xml',
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
