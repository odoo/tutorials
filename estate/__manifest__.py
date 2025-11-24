{
    'name': "Estate",
    'description': """
        Track real estate properties
    """,
    'version': '1.0',
    'author': "sypol",
    'license': "LGPL-3",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
}
