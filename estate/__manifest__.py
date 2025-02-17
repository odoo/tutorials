# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'version': '1.0',
    'summary': 'Real estate internal machinery',
    'description': """
This module contains all the common features of Estate property management.
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
