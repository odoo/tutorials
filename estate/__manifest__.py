{
    'name': 'Real Estate',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',

        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'category': 'Real Estate/Brokerage',
    'application': True,
    'license': 'LGPL-3',
}
