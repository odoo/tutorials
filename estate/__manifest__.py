# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Real Estate',
    'version' : '1.0',
    'category' : 'Real Estate/Brokerage',
    'description' : """
This module provides a real estate services
""",
    'depends' : ['mail'],
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_sequence.xml',
        'data/estate_account_sequence.xml',
        'data/mail_message_subtype_data.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menu.xml',
    ],
    'demo' : [
        'demo/estate.property.type.csv',
        'demo/estate_demo_data.xml',
        'demo/estate_offer_demo_data.xml',
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3',
}
