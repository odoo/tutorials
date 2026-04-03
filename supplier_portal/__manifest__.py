{
    'name': 'Supplier Portal Upload',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Suppliers upload files to create draft invoices',
    'depends': ['portal', 'account', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_view.xml',
        'views/portal_templates.xml',
    ],
    'author': 'VIWAR',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}