# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': "Estate",
    'depends': [
        'base'
    ],
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
        'views/estate_list_view.xml',
        'views/estate_form_view.xml',
        'views/estate_search_view.xml',
        ],
    'installable': True,
    'application': True
}