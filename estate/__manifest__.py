# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage and sell real estate properties',
    'description': """
This module allows users to run real estate agencies. They can advertise and sell estate properties after potential buyers make their offer.
""",
    'version': '1.0',
    'depends': [
        'base',
        'mail',
        'website',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_actions.xml',
        'wizard/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'report/estate_templates.xml',
        'report/estate_reports.xml',
        'views/estate_property_list_template.xml',
        'views/estate_property_detail_template.xml',
        'data/estate_data.xml',
        'data/estate.property.type.csv',
        'data/estate.property.tag.csv',
    ],
    'demo': [
        'demo/estate_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
