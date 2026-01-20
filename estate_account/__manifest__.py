{
    'name': 'estate_account',
    'version': '1.0',
    'sequence': 15,
    'summary': 'estate-account summary',
    'description': "",
    'depends': [
        'estate',
        'account'
    ],
    'data': [
        'views/account_move_views.xml',
        'views/estate_property_views.xml',
        # "security/ir.model.access.csv"
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
