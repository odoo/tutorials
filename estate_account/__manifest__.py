{
    'name': 'Estate Account',
    'version': '1.0',
    'summary': 'Link module between estate and account',
    'description': 'Adds invoicing functionality to the estate module.',
    'category': 'Real Estate',
    'license': 'LGPL-3',
    'author': 'Your Name',
    'depends': ['estate', 'account'],
    'data': [
        'report/estate_property_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
