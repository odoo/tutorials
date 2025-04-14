{
    'name': "Product As Kit",
    'version': '1.0',
    'depends': ['product', 'sale_management'],
    'author': "Rishav Shah",
    'category': 'product',
    'description': """
    Add new new product type as kit
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_views.xml',
    ],
}
