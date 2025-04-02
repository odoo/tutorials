# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sale Order Approval",
    'depends': ['sale'],
    'category': 'Sales/Sales',
    'summary' : "Approval for sale order",
    'version': '1.0',
    'description': """
This module checks for approval before confirming Sale Order
""",
    'author': "shmn-odoo",
    'data': [
        'views/sale_order_views.xml',
    ],
    'auto_install': True,
    'installable' : True,
    'license': 'LGPL-3',
}
