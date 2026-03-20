{
    'name': 'Estate Accounting',
    'version': '1.0',
    'author': 'Odoo S.A.',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,

    'depends': ['account', 'estate'],

    'data': [
        'security/ir.model.access.csv',
    ]
}
