{
    'name': "Real estate",
    'version': '1.0',
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
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
}
