# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate_account',
    'version': '1.0',
    'description': 'Bridge module between estate and account.',
    'depends': ['estate','account'],
    'auto_install': True,
    'license': 'LGPL-3',
    'data': [
        'report/estate_property_templates.xml',
    ]
}
