# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Customer Referral",
    'depends': ['pos_loyalty'],
    'category': 'Sales/Point of Sale',
    'summary': "Referral program for customer",
    'version': '1.0',
    'description': """
This module introduces referral program.
""",
    'author': "shmn-odoo",
    'data': [
        'views/res_partner_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'referral_program/static/src/**/*',
        ]
     },
    'installable': True,
    'license': 'LGPL-3',
}
