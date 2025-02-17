# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Author Name',
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'sequence': 0,
    'license': 'LGPL-3',

    'description': '''
    Description text
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_salesperson.xml',
        'views/estate_menus.xml',

    ],
    'demo': [
    ],
}
