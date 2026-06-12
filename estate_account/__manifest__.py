{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['base', 'estate', 'account'],
    'author': "Asurk",
    'category': 'Real Estate/Brokerage',
    'description': """
    A module so that links the incoive with the real estate module
    """,
    'data': [
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',  # Default License
    'application': True,
    'installable': True,
    # data files always loaded at installation

}
