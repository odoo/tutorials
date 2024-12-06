# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'author': "Aditi Patel",
    'category': 'Real Estate',
    'summary': "Realistic business advertisements",
    'description': "our ultimate real estate spotlight! Effortlessly showcase properties and attract buyers with sleek, engaging ads that sell.",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'auto_install': False
}