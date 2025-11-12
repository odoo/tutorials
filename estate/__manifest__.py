# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Raj Pavara",
    'category': 'Real Estate/Brokerage',
    'description': """
    Basic Real Estate application
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/offer_wizard_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'data/estate_property_type_data.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_list_website_template.xml',
    ],
    'demo': [
        'demo/estate_property_demo.xml'
    ]
}
