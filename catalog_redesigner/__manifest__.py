{
    'name': 'Product Catalog Redesigner',
    'version': '1.0',
    'depends': ['product'],
    'author': 'Shivam Saksham(shsak)',
    'category': 'Sales',
    'description': """
    An module to redesign the catalog in small screens.
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/product_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "catalog_redesigner/static/src/js/product_image.js",
            "catalog_redesigner/static/src/js/image_dialog.js",
            "catalog_redesigner/static/src/xml/product_image.xml",
            "catalog_redesigner/static/src/xml/image_dialog.xml",
            "catalog_redesigner/static/src/scss/styles.scss",
        ],
    },
}
