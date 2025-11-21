{
    'name': "estate_account",
    'version': '18.0',
    'depends': ['estate','account'],
    'author': "Smit",
    'category': 'Real Estate',
    'license' : 'LGPL-3',
    'description': """
        Add property and fees directly to the invoice module.
    """,
    'data': [
        'report/estate_invoice_template.xml'
    ],
    'installable': True,
    'application': True,
}