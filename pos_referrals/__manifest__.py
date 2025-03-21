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
        'report/loyalty_card_report.xml',
        'report/report_data.xml',
        'data/mail_template_data.xml',
        'data/loyalty_program_data.xml',
        'views/res_partner_form.xml',
        'views/loyalty_card_views.xml',
    ],
    'assets': {
        'web.assets_unit_tests':[
            'pos_referrals/static/src/tests/**/*',
        ],
        'point_of_sale._assets_pos': [
            'pos_referrals/static/src/**/*'
        ],
    },
    'installable': True,
    'application': False,
    "license":"LGPL-3"
}
