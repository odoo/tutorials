{
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Accounting Integration for Real Estate',
    'description': """
    This module integrates the Real Estate module with the Accounting module.
    """,
    'author': 'Akya',
    'depends': ['estate', 'account'],
    'data': [
        'report/estate_property_report_invoice.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
