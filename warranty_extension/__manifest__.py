{
    'name': 'Product Warranty',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['sale_management'],
    'license': 'LGPL-3',
    'author' : 'Manthan Akbari',
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'wizards/warranty_wizard_views.xml',
        'views/product_template_views.xml',
        'views/warranty_configuration_views.xml',
        'views/sale_order_views.xml',
        'views/warranty_menu.xml',
    ],
}
