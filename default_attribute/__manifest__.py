{
    'name': 'Default Attribute',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': True
}
