# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'installable' : True,
    'data' : [
        'security/ir.model.access.csv',
        'view/res_users_views.xml',
        'view/property_offer_views.xml',
        'view/property_type_views.xml',
        'view/property_tag_views.xml',
        'view/property_views.xml',
        'view/menus.xml'
    ]
}