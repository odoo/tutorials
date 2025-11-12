{
    'name': "Estate_Account",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['estate', 'account'],
    'author': "Kalpan Desai",
    'category': 'Estate/Accounting',
    'description': """
        Module specifically designed for real estate accounting case.
        This module extends the estate module to include accounting features.
        It allows users to manage financial transactions related to properties,
        such as tracking payments, managing invoices, and handling financial reports.
    """,
    'installable': True,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        ]

}
