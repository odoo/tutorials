# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Product Warranty Management",
    'category': 'Sales/Sales',
    'summary': "Simplify product warranty management.",
    'description': """
A module for managing product warranties
""",
    'version': '1.0',
    'author': "rsbh",
    'depends': ['sale_management'],
    'data': [
          'security/ir.model.access.csv',
          
          'wizard/product_warranty_wizard_views.xml',
          
          'views/sale_order_views.xml',
          'views/product_template_views.xml',
          'views/warranty_configuration_views.xml',
          'views/sale_menus.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
