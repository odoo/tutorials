{
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Estate/Brokerage',
    'summary': 'Link module between Estate and Account',
    'description': 'This module links the Estate and Account modules for financial integration.',
    'depends': ['estate', 'account' ,'mail',
    'spreadsheet_edition',],
    'data': [
        'report/estate_account_templates.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
