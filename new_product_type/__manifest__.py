# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "New Kit Product",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "Raj Pavara",
    'description': """
    New Kit Product
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'wizard/sub_product_wizard_line_views.xml',
        'wizard/sub_product_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    'demo': [
    ]
}
