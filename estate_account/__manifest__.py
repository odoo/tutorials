{
    'name': "Estate Account",
    'version': '1.0',
    'summary': 'A link module between the account and estate modules.',
    'depends': [
        'base',
        'estate',
        'account'
    ],
    'author': "XAFR",
    'license': 'LGPL-3',
    'description': """
    An application module that aims to serve as an onboarding sandbox.
    """,
    'application': "True",
    'data': [
        'security/ir.model.access.csv',
    ],
}
