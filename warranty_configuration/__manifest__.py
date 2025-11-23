# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Warranty Configuration",
    'version': '1.0',
    'depends': ['sale'],
    'author': "Raj Pavara",
    'description': """
Module for add warranty on product
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
        'security/ir.model.access.csv',
        'views/warranty_configuration_views.xml',
        'views/warranty_configuration_actions.xml',
        'views/sale_warranty_configuration_menu.xml',
        'views/sale_order_views.xml',
        'views/warranty_wizard_views.xml',
        'views/warranty_line_wizard_views.xml'
    ]
}
