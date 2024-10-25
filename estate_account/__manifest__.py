{
    'name': "Real Estate Account",
    'version': '1.0',
    'depends': ['estate', 'account'],
    'author': "Harsh Chaudhari",
    'category': 'Category',
    'description': """
    Real Estate Account description...
    """,
    # data files always loaded at installation
    'data': [
        'reports/estate_account_property_invoice.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'application': False,
    'installable': True,
}
