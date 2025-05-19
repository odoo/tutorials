# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Supplier Portal",
    'description':  """
Allows suppliers to upload invoices (PDF & XML) and create draft vendor bills.
""",
    'depends': ['website'],
    'data': [
        'views/supplier_portal_menu.xml',
        'views/supplier_portal_templates.xml'
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3",
}
