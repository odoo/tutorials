{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "gasa",
    'category': 'Real Estate/Brokerage',
    "license": "LGPL-3",
    "application": True,
    "sequence": 1,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/estate_property_rules.xml',
        'data/estate.property.type.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_tag_views.xml',
        'views/inherited_model.xml',
        'views/estate_menus.xml',
        'report/estate_property_offers_report_templates.xml',
        'report/estate_property_reports.xml'
    ],
    "demo": [
        'demo/estate_property_demo_data.xml',
    ],
}
