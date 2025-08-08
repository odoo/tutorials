{
    'name': 'Estate Account',
    'version': '1.0',
    'category': 'Accounting',
    'depends': ['base', 'estate', 'account'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'summary': 'Integration between Estate and Accounting modules.',
    'description': """
        Estate Account Module
        =====================
        This module integrates the Estate module with the Account module.
    """,
    'data': ['report/estate_property_report_inherited.xml']
}
