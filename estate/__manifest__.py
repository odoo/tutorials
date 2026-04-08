{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Asurk",
    'category': 'Real Estate/Brokerage',
    'description': """
    A module so that customers can bid on real estates
    """,
    'data': [
        'security/ir.model.access.csv',
        'security/estate_security.xml',
    ],
    'license': 'LGPL-3',  # Default License
    'application': True,
    'installable': True,
    # data files always loaded at installation

}
