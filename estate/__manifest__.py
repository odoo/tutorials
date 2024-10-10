{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Rajat",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml'

    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': True,
    'installable': True
}