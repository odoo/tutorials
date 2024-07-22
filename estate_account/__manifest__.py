{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['estate', 'account'],
    'author': "Ashutosh Yadav",
    'category': 'Estate Account',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'report/estate_property_with_invoice_templates.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
