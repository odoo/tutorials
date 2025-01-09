{
    'name': 'estate_account',
    'description': "Module that creates invoice once the estate property is marked as sold",
    'installable': True, #Whether a user should be able to install the module from the Web UI or not.
    'application': False, #Whether the module should be considered as a fully-fledged application (True) or is just a technical module (False) that provides some extra functionality to an existing application module.
    'depends': ['account','estate'], # any module necessary for this one to work correctly
    'data': [
        'report/estate_account_templates.xml'    
    ],
    'license':'LGPL-3'
} # type: ignore