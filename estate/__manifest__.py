{
    "name": "Real Estate",
    "description": "This is a real estate listing module.",
    "category": "Real Estate/Brokerage",
    "depends": [
        "base",
        "mail",
        "website"
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/estate_property_multi_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/properties_list_website_template.xml',
        'views/estate_menus.xml',
        'views/website_menus.xml',
        'views/res_config_settings_views.xml',
        'data/estate.property.type.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml'
    ],
    'demo': [
        'demo/estate_property_data.xml',
        'demo/estate_property_offer_data.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'application': True
}
