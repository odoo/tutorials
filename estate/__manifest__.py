{
    'name': 'Real Estate',
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
}
