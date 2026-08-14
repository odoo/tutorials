{
    'name': "My super Real Estate App",
    'version': '1.0',
    'depends': ['base'],
    'author': "matho",
    'description': """
    Voici ma nouvelle application
    """,
    'application': True,
    'installable': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
    # data files containing optionally loaded demonstration data
}
