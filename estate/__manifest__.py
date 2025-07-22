{
    'name': "Real Estate",
    'summary': "Manage real estate properties, offers, and sales in Odoo",
    'category': "Real Estate/Brokerage",
    'description': (
        "This module allows you to manage real estate properties, offers, property types, and related data. "
        "It includes basic listing management, offer tracking, reporting capabilities, and user access controls. "
        "Suitable for use in property management workflows within the Odoo system."
    ),
    'author': "Dhruvrajsinh Zala (zadh)",
    'installable': True,
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_templates.xml',
        'report/estate_user_properties_templates.xml',
        'report/estate_user_properties_report.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offers.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.types.csv',
    ],
    'demo': ['demo/demo_data.xml'],
    'license': 'AGPL-3'
}
