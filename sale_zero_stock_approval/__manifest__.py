{
    'name': 'Sale Zero Stock Approval',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Maan Patel',
    'summary': 'Adds zero stock approval feature to sale orders',
    'description': """
        This module adds a zero stock approval feature to sale orders.
        - Allows sales administrators to approve orders with zero stock
        - Read-only for sales users
    """,
    'depends': ['sale'],
    'data': ['views/sale_order_view.xml',],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3'
}
