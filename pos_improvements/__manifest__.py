# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name':'POS Improvements',
    'version':'1.0',
    'depends': ['point_of_sale'],
    'description':"""
Allow pos users to pay from ticketscreen.
""",
    'installable': True,
    'application' : True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_improvements/static/src/**/*',
        ],
    },
    'license':'LGPL-3',
}
