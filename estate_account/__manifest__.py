# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Real Estate Invoicing",
    'category': "Accounting",
    'summary': "Manage Real Estate Invoices",
    'description': """
    This module allows the users to manage their real estate invoices.
    """,
    'depends': [
        'estate',
        'account',
    ],
    'data': [
        'report/estate_property_report.xml',
    ],
    'license': "LGPL-3",
}
