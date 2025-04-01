# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Book Price",
    'version': "1.0",
    'category': "Sales/Sales",
    'description': """
        On sale order line and invoice line show price list price.
    """,
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml'
    ],
    'installable': True,
    'license': "LGPL-3",
}
