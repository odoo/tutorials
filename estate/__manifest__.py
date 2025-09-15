# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate',
    'version': '0.0.1',
    'category': 'Sales',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/estate_property_views.xml',
        ],
    'summary': 'Real Estate Module - Training',
    'website': 'https://www.odoo.com/jobs',
    'installable': True,
    'application': True,
    'author': 'Jérémie Parisel',
    'license': 'LGPL-3',
}
