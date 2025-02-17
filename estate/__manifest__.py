{
    "name": "Real Estate",
    "description": "This is a real estate listing module.",
    "category": "Real Estate/Brokerage",
    "depends": [
        "base",
        "mail"
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml'
    ],
    'demo': [
        'demo/estate_property_data.xml',
        'demo/estate_property_offer_data.xml'
    ],
    'license': 'LGPL-3',
    'application': True
}
