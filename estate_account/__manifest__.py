{
    'name': 'Estate Account Integration',
    'version': '1.0',
    'summary': 'Integration between Estate and Accounting modules',
    'description': 'This module creates invoices for sold properties.',
    'category': 'Accounting',
    'author': 'yasp',
    'depends': ['estate', 'account'],
    'license': 'LGPL-3',
    'data': [
        'report/estate_property_report.xml',
    ],
    'installable': True,
    'application': False,
}
