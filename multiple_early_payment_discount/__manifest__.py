{
    'name': "Multiple Early Payment Discount",
    'category': "Accounting",
    'depends': ['accountant', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_term_views.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': "LGPL-3"
}
