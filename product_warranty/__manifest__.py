{
    'name': 'Products Warranty',
    'category': 'Sales/Warranty',
    'depends': ['sale'],
    'data' : [
        'security/ir.model.access.csv',
        'data/warranty_product_data.xml',
        'views/product_views.xml',
        'views/warranty_config_views.xml',
        'views/product_warranty_menu.xml',
        'views/sale_order_views.xml',
        'wizard/product_warranty_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
