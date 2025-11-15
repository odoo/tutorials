# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Book Price",
    'category': 'Sales/Sales',
    'description':  """
This is the add-on module that enables 'Book Price' field into order lines of Sales Orders and Invoicing to let the client know of actual price and adjusted price.
""",
    'depends':['sale_management'],
    'data': [
        'views/sale_order_line.xml',
        'views/account_move_line.xml',
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3",
}
