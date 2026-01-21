{
    'name': "Real estate",
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'application': True,
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ]
}
