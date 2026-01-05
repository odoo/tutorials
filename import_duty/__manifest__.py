{
    'name': 'Import Duty',
    'category': 'Tutorials/Import',
    'version': '1.0',
    'sequence': 1,
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'summary': 'Help users with Import-Export.',
    'depends': ['accountant', 'l10n_in'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/account_move_views.xml',
        'wizards/wizard_views.xml'
    ],
}
