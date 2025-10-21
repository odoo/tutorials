# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate',
    'version': '0.1',
    'application': True,
    'author': 'matho',
    'depends': [
        'base',
    ],
     'data': [
        'security/ir.model.access.csv',  
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
      ]
}