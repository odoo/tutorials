{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'mail', 'website'],
    'author': "Vaidik Gorasiya - vrgo",
    'description': """
        This module is designed to manage real estate properties.
        It allows users to store detailed information about properties,
        such as name, description, price, living area, and more.
    """,
    'category': 'Real Estate',
    'data': [
        'security/property_security.xml',
        'security/ir.model.access.csv',
        'security/property_rules.xml',
        'wizard/estate_property_offer_wizard_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_website.xml',
        'data/estate_property_data.xml'
    ],
    'demo': [
        'data/estate_property_demo.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}
