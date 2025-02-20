# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate APP',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage Real Estate Properties',
    'description': """
    This module allows the users to manage their real estate properties.
    It also enables them to advertise them.
    """,
    'version': '1.0',
    'depends': ['base', 'web', 'website'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',

        'report/estate_property_report_templates.xml',
        'report/estate_property_report_views.xml',

        'data/master_data.xml',

        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/website_property_views.xml',
        'views/website_property_list_detail_views.xml',
        'wizard/estate_property_offer_wizard_views.xml',

        'views/website_menus.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
