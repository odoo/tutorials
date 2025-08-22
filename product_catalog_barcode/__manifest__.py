{
    "name": "Product Catalog Barcode",
    "version": "1.0",
    'description': """
        Handle product catalog with barcode
    """,
    "depends": ["sale_management", "purchase", "barcodes"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "product_catalog_barcode/static/src/scanned_products.js",
            "product_catalog_barcode/static/src/kanban_controller.js",
            "product_catalog_barcode/static/src/kanban_model.js",
            "product_catalog_barcode/static/src/kanban_record.js",
        ],
    },
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
}
