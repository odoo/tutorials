# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate Accounting',
    'version': '1.9',
    'author': 'Abo Taha',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,

    'depends': ['account', 'estate'],

    'data':[
        'security/ir.model.access.csv',
    ]
}