{
    'name': 'estate_crm',
    'version': '1.0',
    'category': 'Tutorials',
    'Summary': 'Leads addon for estate',
    'description': 'Manage your estate leads',
    'installable': True,
    'author': 'times',
    'website': 'https://www.odoo.com/app/health',
    'depends': [
        'estate',
        'crm',
    ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
    ],
}
