{
    'name': "Book Price (Pricelist Price)",
    'version': '1.0',
    'depends': ['base', 'sale_management'],
    'author': "ppch",
    'category': 'Category',
    'description': """
    Book Price (Pricelist Price) on sales order lines and invoice lines
    which will be used to compare between Book Price (Pricelist Price) and
    manually adjusted price on the lines.
    """,
    'license': "LGPL-3",
    'data': [
        'views/sale_order_line_views.xml',
        'views/account_move_line_views.xml',
    ],
    'installable': True,
}
