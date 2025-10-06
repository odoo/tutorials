{
    'name': 'Real Estate Account',
    'version': '1.0',
    'summary': 'Link between Real Estate and Accounting',
    'description': """
        This module links the Real Estate module with Accounting,
        automatically creating invoices when properties are sold.
    """,
    'depends': ['estate', 'account'],
    "category": "Sales",
    'installable': True,
    'application': True,
    'auto_install': True,
    "license": "LGPL-3",
}
