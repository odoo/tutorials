{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mohamed Yousef",
    'category': 'Sales',
    'description': """
    A Real Estate App to ....
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    "license": "LGPL-3"
}
