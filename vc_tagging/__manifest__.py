# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'V&C Tagging',
    'version': '1.0',
    'description' : """
Automates dropshipping by tagging vendor and customer in SO, PO and Picking.
""",
    'depends': ['contacts', 'purchase', 'sale_management', 'stock'],
    'data': [
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
