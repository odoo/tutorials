# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'category':'module_category_real_estate_brokerage',
    'license': 'LGPL-3',
    'version' : '1.0',
    'depends': [
        'base'
    ],
    "data": [
         'security/ir.model.access.csv',
         'views/estate_property_tag.xml',
         'views/estate_property_offer_action.xml',
         'views/estate_property_type_action.xml',
         'views/estate_property_view.xml',
         'views/res_users_inherit.xml',
         'views/estate_menu.xml'
    ],
    'installable': True,
    'application': True,
}