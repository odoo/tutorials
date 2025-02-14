{
    'name': "estate",
    'version': '18.0',
    'depends': ['base'],
    'author': "Smit",
    'category': 'Real Estate',
    'license' : 'LGPL-3',
    'description': """
        Buy and sell properties.
    """,
    'data': [
        'security/ir.model.access.csv',
        'security/estate_security.xml',
        'views/estate_actions.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
}
