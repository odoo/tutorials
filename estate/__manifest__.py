# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name':'Real Estate',
    'version':'1.0',
    'category':'Real Estate/Brokerage',
    'author':'JODH',
    'depends': ['mail', 'website', 'rating'],
    'description':"""
This Module provides real estate advertisements
""",
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_sequence.xml',
        'data/mail_rating_data_template.xml',
        'data/mail_message_subtype_data.xml',
        'data/estate_property_website_data.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/rating_rating_views.xml',
        'views/estate_property_template.xml',
        'views/estate_property_menus.xml',
    ],
    'demo':[
        'demo/estate.property.type.csv',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'application':True,
    'installable': True,
    'license':'LGPL-3',
}
