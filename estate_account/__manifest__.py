# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate Accounting',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'estate',
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/estate_property_views.xml',
        'report/estate_reports.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': True,
}
