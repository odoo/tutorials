{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Harsh Chaudhari",
    'category': 'Category',
    'description': """
    Real Estate description...
    """,
    # data files always loaded at installation
    'data': [
        'views/estate_property_offers_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_views.xml',
        'views/estate_menus_view.xml',
        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': True,
    'installable': True,
}
