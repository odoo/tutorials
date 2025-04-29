{
    'name': 'Product Warranty',
    'version': '1.0',
    'depends': ['sale_management'],
    'description': """
        This module adds warranty availabe feature for products.
        """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/add_warranty_wizard_views.xml',
        'views/product_template_views.xml',
        'views/warranty_config_views.xml',
        'views/warranty_config_menu.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3'
}
