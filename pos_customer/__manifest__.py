{
    'name': 'POS Customer Display',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'author': 'matd',
    'category': 'Category',
    'description': """
It provides POS customer display module
""",
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets_prod': [
            'pos_customer/static/src/pos_order.js',
        ],
        'point_of_sale.customer_display_assets': [
            'pos_customer/static/src/customer_display/*',
        ],
    },
    'license': 'LGPL-3',
}
