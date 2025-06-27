{
    'name': "Book Pricelist",
    'category': '',
    'version': '0.1',
    'depends': ['sale'],
    'sequence': 1,
    'application': True,
    'installable': True,
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_view.xml',
    ],
    'license': 'AGPL-3'
}
