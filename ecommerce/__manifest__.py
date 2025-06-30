{
    'name': 'E-commerce',
    'version': '1.0',
    'category': 'Website',
    'summary': 'E-commerce module for managing products and categories',
    'description': """
        This module provides basic e-commerce functionalities including product management and category organization.
    """,
    'depends': "",
    'data': [
        'security/ir.model.access.csv',
        'views/ecommerce_product_category_views.xml',
        'views/ecommerce_product_views.xml',
        'views/ecommerce_product_menus.xml',
        
    ],
    'installable': True,
    'application': True,
    
}