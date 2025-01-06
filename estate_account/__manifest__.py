{
    'name': 'estate_account',
    'installable': True, #Whether a user should be able to install the module from the Web UI or not.
    'application': False, #Whether the module should be considered as a fully-fledged application (True) or is just a technical module (False) that provides some extra functionality to an existing application module.
    'depends': ['account','estate'], # any module necessary for this one to work correctly
    'data': [
        'security/ir.model.access.csv', #security access
        'views/estate_account_views.xml',
        'views/estate_account_menus.xml',
    ],
    'license':'LGPL-3'
}