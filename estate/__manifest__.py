# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate APP',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage Real Estate Properties',
    'description': """
    This module allows the users to manage their real estate properties.
    It also enables them to advertise them.
    """,
    'version': '1.0',
    'depends': ['base', 'web'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
