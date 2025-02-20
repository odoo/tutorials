{
    'name': 'Real Estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
