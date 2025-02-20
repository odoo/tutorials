# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sale Product Kit",
    'category': 'Sales/Sales',
    'summary': "Create and sell products of type kit",
    'description': """
This bridge module adds the ability to create and sell products of type kit.
    """,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/edit_sub_product_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/sale_portal_templates.xml',
        'report/sale_order_report_templates.xml',
        'report/account_invoice_report.xml',
    ],
    'demo': [
        'demo/sale_product_kit_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
