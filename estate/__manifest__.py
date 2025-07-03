{
    'name': 'Real Estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',

        'report/estate_property_offer_templates.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/res_users_templates.xml',
        'report/res_users_reports.xml',

        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml',
    ],
    'application': True,
    'license': 'AGPL-3'
}
