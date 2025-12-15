# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate Advertisement',
    'version': '1.0',
    'author': 'Odoo',
    'category': 'Sales/Real Estate',
    'sequence': 15,
    'summary': 'Manage property listings and real estate advertisements',
    'description': """
Real Estate Advertisement Management
====================================
This module allows you to manage real estate properties, including:
    * Property listings with detailed information
    * Property types and tags
    * Property offers and negotiations
    * Sales tracking
    """,
    'depends': ['base'],
    'data': [
                'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
