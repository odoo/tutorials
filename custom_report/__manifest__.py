{
    'name': 'Custom Picking Report',
    'version': '1.0',
    'summary': 'Add a custom report in sales module',
    'description': """
Checking Product Quantity
==========================
In this module, add a custom report in which no sub kitt product will not print in report.

    """,
    'author': 'Raghav Agiwal',
    'depends': ['sale_management', 'mrp', 'website'],
    'data': [
        'report/custom_report_mo_views.xml',
        "report/custom_report_views.xml"
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
