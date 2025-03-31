{
    'name': 'Product Warranty',
    'version': '1.0',
    'category': 'Sales/Product Warranty',
    'description': 'This module adds warranty to products based on the percentage of the price of product.',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_warranty_configuration_views.xml',
        'wizard/add_product_warranty_views.xml',
        'views/sale_order_views.xml',
        'views/product_warranty_configuration_menu.xml',
    ],
    'demo': [
        'demo/warranty_configuration_demo.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
