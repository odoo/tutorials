{
    'name': 'Product Warranty',
    'description': 'Product Warranty Module',
    'sequence': 1,
    'version': '1.0',
    'depends': ['sale_management'],
    'author': 'Shiv Bhadaniya',
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'wizard/warranty_wizard_views.xml',
        'views/product_template_views.xml',
        'views/product_warranty_views.xml',
        'views/product_warranty_menus.xml',
        'views/sale_order_views.xml',
    ],
}
