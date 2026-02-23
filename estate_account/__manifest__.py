{
    'name': "Real Estate Invoicing",
    'depends': ['base', 'estate', 'account'],
    'author': "Odoo",
    'category': 'Category',
    'license': 'LGPL-3',
    'application': True,
    'description': """
    A app for real estate invoices.
    """,
    'data': [
        'views/estate_account_form_views.xml',
    ],
}
