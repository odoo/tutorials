{
    'name': 'pricelist_price',
    'author': 'soham',
    'version': "1.0",
    'description': 'Added pricelist price',
    'depends': ['sale_management'],
    'license': 'LGPL-3',
    'data': [
        'views/account_move_line_view.xml',
        'views/sale_order_line_view.xml'
    ],
    'application': True,
    'installable': True,
    'auto-install': True,
}
