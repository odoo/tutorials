{
    'name': 'Add pricelist price',
    'description': 'Book Price for Sales and Accounting',
    'version': '1.0',
    'author': 'habar',
    'depends': ['sale', 'account'],
    'data': [
        'views/sale_order_line_views.xml',
        'views/account_move_line_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
