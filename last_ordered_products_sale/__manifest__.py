{
    'name': "Last Ordered Products (Sale)",
    'version': '1.0',
    'depends': ['last_ordered_products', 'sale_management'],
    'author': "Parthav Chodvadiya (PPCH)",
    'category': '',
    'description': """
    Show last ordered products for customers in sale order
    """,
    'data': [
        'views/sale_order_form.xml',
        'views/account_move_form.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': True,
}
