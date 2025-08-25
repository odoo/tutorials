# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'ESTATE',
    'version': '1.0',
    'category': 'Estate',
    'sequence': 15,
    'summary': 'Module to track all things related to real estate of any company',
    'description': "",
    'website': 'https://www.odoo.com/page/estate',
    "application": True,
    'depends': [
        'base'
    ],
    'data': [
        "security/ir.model.access.csv"
    ],
    'demo': [
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False
}
