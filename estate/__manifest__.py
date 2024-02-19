# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'depends': [
        'base'
    ],
    'category': 'Tutorials/Real Estate',
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}