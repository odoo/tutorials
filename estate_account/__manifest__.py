{
    'name' : 'Real Estate Account',
    'version' : '1.0',
    'author' : 'odoo',
    'depends' : ['estate', 'account'],
    'data' : [
        'views/estate_property_views.xml',
        'views/account_invoice_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}