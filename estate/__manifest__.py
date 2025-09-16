# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate',
    'depends': [
        'base',
    ],
    'version': '19.0.0.0',
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml', # depends on estate_property_views.xml, estate_property_type_views.xml
        'security/ir.model.access.csv',
    ]
}