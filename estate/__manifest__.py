{
    'name': "Real Estate",
    'depends': ['base', 'mail', 'website'],
    'application': True,
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_menus.xml'
    ],
    'demo': [
        'demo/demo_data.xml'
    ]
}
