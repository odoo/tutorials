{
    'name': "real estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "elsa ringling (elrin)",
    'category': 'Services',
    'description': """
    This is a test module for the server framework 101 tutorial
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.access.csv'
    ],
    # data files containing optionally loaded demonstration data

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
