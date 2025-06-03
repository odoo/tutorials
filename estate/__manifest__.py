# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'category': 'Real Estate/Brokerage',
    'summary': "Manage and sell real estate properties",
    'description': """
This module allows users to run real estate agencies. They can advertise and sell real estate properties by accepting offers made by buyers.
    """,
    'version': '1.0',
    'depends': [
        'base',
        'mail',
        'website',
    ],
    'data': [
        'security/estate_groups.xml',
        'security/estate_property_security.xml',
        'security/ir.model.access.csv',
        'wizard/estate_property_add_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'views/estate_property_templates.xml',
        'report/estate_templates.xml',
        'report/estate_reports.xml',
        'data/estate_data.xml',
        'data/estate_property_type_data.xml',
        'data/estate_property_tag_data.xml',
    ],
    'demo': [
        'demo/estate_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
