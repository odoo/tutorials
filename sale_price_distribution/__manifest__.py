# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Price Distribution',
    "summary": "Adds a wizard to distribute the sale price among other order lines",
    'category': 'Sale/Sale Price',
    'version': '1.0',
    'depends': ['base','sale','sale_management'],
    'data': [
        "security/ir.model.access.csv",
        'views/sale_order_views.xml',
        'wizard/cost_distribution_wizard.xml'
    ],
    "license": "LGPL-3",
    'installable': True,
    'application': False,
}
