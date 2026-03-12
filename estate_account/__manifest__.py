{
    'name': 'Real Estate Account',
    'version': '1.1',
    'summary': 'Module to Mangage Real Estate Property Listings',
    'website': 'https://www.odoo.com/app/estate',
    'depends': [
        'base',
        'estate',
        'account',
    ],
    'data': [
        'report/estate_account_template.xml',
    ],
    'application': True,
    'author': 'kapat-odoo',
    'license': 'LGPL-3',
}
