# -*- coding: utf-8 -*-

{
    'name': "POS Referrals",
    'summary': "Referral Gift cards for customers",
    'description': """
    Allow customers to refer other customers in POS
    """,
    'author': "Devmitra sharma (dvsh)",
    'category': 'Point of Sale',
    'depends': ['loyalty','point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/loyalty_card_views.xml',
        'views/res_partner_form.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_referrals/static/src/**/*'
        ],
    },
    'installable': True,
    'application': False,
    "license":"LGPL-3"
}
