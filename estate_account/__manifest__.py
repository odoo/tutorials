{
    'name': "Real Estate Accounting Link",
    'summary': "Link estate and account modules for creating invoice",
    'description': """
This module is used as a bridge between estate and account modules in order to create an invoice automatically when marking a property as sold
    """,
    'author': 'Odoo',
    'version': '1.0',
    'depends': [
        'estate',
        'account',
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'license': 'LGPL-3',
}
