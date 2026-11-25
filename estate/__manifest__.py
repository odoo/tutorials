{
    'name': "Real estate",
    'depends': ['base'],
    'author': "Author Algue",
    'category': 'Category',
    'description': """
    Description Real Estate App
    """,
    'application': True,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'security/ir.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
}
