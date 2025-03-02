{
    'name': 'Stock Warranty',
    'version': '1.0',
    'summary': 'Adds Warranty associating with the product',
    'author': 'Harsh Shah',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_warranty_wizard_view.xml',
        'views/sale_warranty_configuration_view.xml',
        'views/sale_warranty_menus.xml',
        'views/sale_order_views.xml',
        'views/product_template_view.xml',
    ],
    'demo': [
        'demo/product_product_demo.xml',
        'demo/warranty_configuration_demo.xml'
    ]
}
