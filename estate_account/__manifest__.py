# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate Account',
    'depends': ['estate', 'account'],
    'version': '1.0',
    'summary': 'Enables invoicing for Estate properties',
    'description': """
This module contains all the feature needed for invoicing estate properties.
    """,
    'data': [
        'report/estate_account_templates.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
