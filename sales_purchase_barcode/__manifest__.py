{
    "name": "SO/PO Barcode Scanning",
    "version": "1.0",
    "category": "Sales",
    "summary": "Adds products to SO from catalog via barcode scanning.",
    "author": "Kalpan Desai",
    "depends": ["sale_management", "web", "product", "purchase", "barcodes"],
    "license": "LGPL-3",
    "assets": {
        "web.assets_backend": [
            "sales_purchase_barcode/static/src/**/*"
        ]
    },
    "installable": True,
    "application": True,
}
