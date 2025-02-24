# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'depends': ['base', 'website'],
    'category': 'Real Estate/Brokerage',
    'summary': 'Real estate internal machinery',
    'version': '1.0',
    'description': """
This module contains all the common features of Estate property management.
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate_property_type_data.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/website_property.xml',
        'views/website_property_details.xml',
        'views/website_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
    ],
    'demo': [
        'demo/property_demo.xml',
        'demo/offer_demo.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
