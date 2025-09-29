{
    'name': 'Estate',
    'summary': 'Sell real estate properties',
    'category': 'Real Estate/Brokerage',
    'depends': ['base', 'web'],
    'application': True,
    'auto_install': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/menus.xml',
    ],
}
