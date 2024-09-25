{
    'name': 'Product Warranty Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage product warranties in sales',
    'description': """
    This module adds warranty configuration to products in the sales module.
    """,
    'depends': ['stock', 'website_sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_warranty_wizard_view.xml',
        'views/sale_oder_line_view.xml',
        'views/product_warranty_view.xml',
        'views/menu.xml',
        'data/warranty_data.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
