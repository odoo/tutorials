{
    'name': 'Real Estate',
    'author': 'zavan',
    'depends': ['base'],
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'report/res_users_templates.xml',
        'report/res_users_reports.xml'
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate.property.xml',
        'demo/estate.property.offer.xml'
    ]
}
