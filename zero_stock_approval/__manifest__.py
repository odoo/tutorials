# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Zero Stock Approval',
    'version': '1.0',
    'depends': ['sale_management'],
    'description': """
This module adds a zero stock approval feature to sale orders.
-Group of Sales/User can only read the approval field. Without approval sale order can't be confirmed.
""",
    'data' : [
        'views/sale_order_view.xml'
    ],
    'license' : 'LGPL-3'
}
