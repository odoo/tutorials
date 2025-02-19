{
    'name': "Real Estate",
    'description': """ The Real Estate Advertisement module. """,
    'license': 'LGPL-3',
    'application': True,
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_controllor_templates.xml',
        'data/estate.property.type.csv',
        'report/estate_offer_report_templates.xml',
        'report/estate_offer_reports.xml',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ]

}
