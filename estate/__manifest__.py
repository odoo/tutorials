{
    'name': "Real Estate Management",
    'depends': ['base'],
    'author': "Olivier Renson",
    'application': True,
    'license': "AGPL-3",
    'data': [
        'data/estate.property.type.csv',
        'data/estate.property.tag.csv',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_user_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate.property.xml',
    ]
}
