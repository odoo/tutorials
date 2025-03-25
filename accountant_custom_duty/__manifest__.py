{
    'name': 'Custom duty on Import and Export',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['accountant', 'l10n_in'],
    'auto_install': True,
    'application': True,
    'data':[
        'security/ir.model.access.csv',

        'wizard/account_bill_of_entry_wizard.xml',
        
        'views/account_move_views_inherit.xml',
        'views/res_config_settings_views.xml'
    ]
}
