{
    'name': 'Estate Account',
    'version': '1.0',
    'description': """
    This module allows the creation of the invoice when a property is marked as Sold
    """,
    'depends': ['base', 'estate', 'account'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
