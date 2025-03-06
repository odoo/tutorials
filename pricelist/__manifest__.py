{
    'name': 'PriceList',
    'version': '1.0',
    'depends': ['base', 'sale_management'],
    'author': 'matd',
    'description': """
Add pricelist price
""",
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
