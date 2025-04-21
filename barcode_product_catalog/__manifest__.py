{
    'name': "Product Catalog Barcode",
    'version': '1.0',
    'depends': ['stock_barcode', 'stock', 'sale_management', 'purchase'],
    'author': "Rishav Shah",
    'category': 'product',
    'description': """
    Scan Barcode to add product to order line from product catalog
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'barcode_product_catalog/static/src/**/*',
        ],
    },
}
