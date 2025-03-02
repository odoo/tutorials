# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Product Warranty",
    'depends': ['sale_management'],
    'summary' : "Warranty for product",
    'version': '1.0',
    'description': """
This module allows user to add warranty to products
""",
    'author': "shmn-odoo",
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/warranty_configuration_views.xml',
        'wizard/warranty_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable' : True,
    'license': 'LGPL-3',
}
