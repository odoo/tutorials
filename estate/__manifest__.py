{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Harsh Chaudhari",
    'category': 'Category',
    'description': """
    bla bla bla description...
    """,
    # data files always loaded at installation
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,  
}