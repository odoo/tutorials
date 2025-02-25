{
    'name': "Book Price Pricelist",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'account'],
    'author': "ppch",
    'category': 'Category',
    'description': """
    Book Price on Sales order line and accunt move line
    """,
    'license': "LGPL-3",
    'data': [
        'views/sale_order_line_views.xml',
        'views/account_move_line_views.xml',
    ],
    'installable': True,
}