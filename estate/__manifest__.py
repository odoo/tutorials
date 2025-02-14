{
    'name': "Real Estate",
    'description': """ The Real Estate Advertisement module. """,
    'license': 'LGPL-3',
    'application': True,
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],

}
