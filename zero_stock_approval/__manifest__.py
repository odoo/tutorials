# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Zero Stock Approval',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Add zero stock approval field to sale orders',
    'description': """
        This module adds a Zero Stock Approval field to sale orders that:
        - Allows confirming sale orders with zero stock when approved
        - Is read-only for Sales/User
        - Is accessible for Sales/Administrator
    """,
    'author': 'nmak',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
