{
    'name': 'Dev Zero Stock Blockage',
    'version': '1.0',
    'summary': 'Add zero stock blockage feature to sale order',
    'description': """
Checking Product Quantity
==========================
This module stops Sales Orders from being confirmed if any product is out of stock, unless a Sales Manager gives approval.

Sales users can see the Zero Stock Approval field but cannot edit it.

It only checks stock for physical products, not services or combos.
    """,
    'author': 'Raghav Agiwal',
    'depends': ['sale_management', 'stock'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
