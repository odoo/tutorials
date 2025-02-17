{
    'name': 'Real Estate',
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menus.xml',
        'data/estate.property.type.csv',
        'report/estate_reports.xml',
        'report/estate_report_views.xml',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
    ],
    'installable': True,
    'application': True,
}
