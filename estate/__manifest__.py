# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': "Estate",
    'depends': [
        'base'
    ],
    'data':[
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
        ],
    'installable' : True,
    'application' : True
}