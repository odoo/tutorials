# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'version': '0.1',
    'category': 'estate',
    'summary': 'Sell real estate properties',
    'description': "",
    'depends': ['base'],
    'website': 'https://www.odoo.com/page/estate',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/menus.xml',
    ],
}
