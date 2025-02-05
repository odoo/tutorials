# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'category':'module_category_real_estate_brokerage',
    'depends': [
        'base'
    ],
    "data": [
         'security/ir.model.access.csv',
         'views/estate_property_view.xml',
         'views/estate_menu.xml'
    ],
    'installable': True,
    'application': True,
}