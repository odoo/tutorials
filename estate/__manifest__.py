{
    'name': "estate",
    'version': '18.0',
    'depends': ['base','account'],
    'author': "Smit",
    'category': 'Real Estate/Brokerage',
    'license' : 'LGPL-3',
    'description': """
        Buy and sell properties.
    """,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_actions.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'demo/estate.property.type.csv',
        'demo/estate_property.xml',
    ],
    'installable': True,
    'application': True,
}
