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
    'installable': True,
    'application': False,
}