{
    'name': 'estate_account',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'estate',
        'account',
    ],
    'data': [
        'ir.model.access.csv',
        'views/estate_account_views.xml',
        'views/estate_account_menus.xml',
    ],
    'application': True
}
