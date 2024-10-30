{
    'name': "estate",
    'version': '1.0',
    'depends': ['base', 'mail', 'website'],
    'author': "srap",
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'wizard/add_offer_wizard_view.xml',
        'reports/report_estate_property_template.xml',
        'reports/report_users_estate_properties_template.xml',
        'reports/estate_property_reports.xml',
        'views/templates.xml',
        'views/res_users_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml',
    ],
    "demo": [
        'data/estate.property.type.csv',
        "demo/demo_data.xml",
    ],
    'application': True
}
