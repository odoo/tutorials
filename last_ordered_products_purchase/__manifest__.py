{
    'name': "Last Ordered Products (Purchase)",
    'version': '1.0',
    'depends': ['last_ordered_products', 'purchase'],
    'author': "Parthav Chodvadiya (PPCH)",
    'category': '',
    'description': """
    Show last ordered products for vendors in purchase order
    """,
    'data': [
        'views/purchase_order_form.xml',
        'views/account_move_form.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': True,
}
