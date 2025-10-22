{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'author': "Jeanne Delneste",
    'license': "LGPL-3",
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_user_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv'
    ],
}
