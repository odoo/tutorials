# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base'],
    'icon': '/real_estate/static/description/estate_icon.png',
    'author': 'Odoo',
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_properties_offer_views.xml',
        'views/estate_properties_views.xml',
        'views/estate_properties_type_views.xml',
        'views/estate_properties_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_properties_menus.xml',
        'data/master_data.xml',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
