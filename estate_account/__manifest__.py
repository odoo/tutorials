{
    'name': "estate account",
    'version': '1.0',
    'depends': [
        'estate',
        'account'],
    'author': "elsa ringling (elrin)",
    'category': 'Accounting',
    'description': """
    This is a test module for the server framework 101 tutorial
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.access.csv',

        'views/estate_account_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
