# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name':'Pos second UOM',
    'version':'1.0',
    'author':'JODH',
    'depends': ['point_of_sale', 'uom'],
    'description':"""
This Module provides second uom for pos
""",
    'data':[
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_second_uom/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license':'LGPL-3',
}
