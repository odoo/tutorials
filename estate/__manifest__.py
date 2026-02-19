{
    'name': "Real Estate Management",
    'depends': ['base'],
    'author': "Olivier Renson",
    'application': True,
    'license': "AGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_user_views.xml',
        'views/estate_menus.xml',
    ]
}
