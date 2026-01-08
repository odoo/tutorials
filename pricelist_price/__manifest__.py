{
    'name': 'Pricelist Price',
    'sequence': 1,
    'category': 'Tutorials/pricelist_price',
    'version': '1.0',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale_management',
        'account'
    ],
    'data' : [
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
    ]
}