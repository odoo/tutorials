{
    'name': 'warranty',
    'version': '1.0',
    'depends': ['sale_management'],
    'author': 'Odoo - Rushil Patel',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'wizard/sale_order_warranty_views.xml',

        'views/product_template_views.xml',
        'views/warranty_config_views.xml',
        'views/warranty_config_menu.xml',
        'views/sale_order_views.xml',
    ]
}
