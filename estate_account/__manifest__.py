{
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Estate',
    'summary': 'Integration between Estate and Accounting',
    'description': """
        This module integrates the Estate module with the Accounting module.
    """,
    'depends': ['estate', 'account'],
    'data': [
        'views/estate_property_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': "AGPL-3"
}
