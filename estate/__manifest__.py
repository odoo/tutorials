# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': 'Author Name',
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'sequence': 0,
    'license': 'LGPL-3',

    'description': '''
    Description text
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_user_reports.xml',
        'report/estate_property_user_templates.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_salesperson.xml',
        'views/estate_menus.xml',
        'data/master_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
        'demo/demo_offer_data.xml'
    ]
}
