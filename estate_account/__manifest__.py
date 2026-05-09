{
    'name': 'estate_account',
    'version': '1.0',
    'category': 'Tutorials',
    'Summary': 'Invoicing addon for estate',
    'description': 'Manage your estate invoice',
    'installable': True,
    'author': 'times',
    'website': 'https://www.odoo.com/app/health',
    'depends': [
        'estate',
        'account',
        'calendar',
    ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
    ],
}
