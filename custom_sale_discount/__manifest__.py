# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Sale Order Discount',
    'version': '1.0',
    'depends': ['sale', 'sale_management'],
    'author': 'Nisarg Mistry',
    'category': 'Sales',
    'summary': 'Automatically reapply global discount when subtotal changes',
    'description': 'This module recalculates the global discount in sale orders whenever the subtotal changes.',
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
