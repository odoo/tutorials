{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "pirth",
    'category': 'Tutorial',
    'application': True,
    'installable': True,
    'summary': "Real estate",
    'description': """
    Module about real estate
    """,
    'license': "LGPL-3",
    # beware the order of the data imports !
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ]
}
