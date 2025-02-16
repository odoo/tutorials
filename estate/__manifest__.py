{
    'name': "Real Estate",
    'depends': ['base', 'mail'],
    'application': True,
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ]
}
