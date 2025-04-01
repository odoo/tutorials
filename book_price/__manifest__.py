# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Book Price",
    'version': '1.0',
    'depends': ['sale'],
    'author': "Raj Pavara",
    'description': """
Module for add book price on sale order lines and invoice lines
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml'
    ]
}
