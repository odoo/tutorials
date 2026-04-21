{
    'name': "Estate",
    'version': '69.0',
    'depends': ['base'],
    'author': "Stef Ossé",
    'category': 'Category',
    'description': """
    A specialized application for **estate management**.
    """,
    # data files always loaded at installation
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': True
}
