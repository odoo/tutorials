{
    'name': "Partial Payment",
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'description': "Adds new Partial Payment Feature for multiple bill/invoice",
    'depends': [
        'account',
        'accountant'
    ],
    'data': [
        'security/ir.model.access.csv',

        'wizard/account_payment_register_views.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
}
