{
    "name": "Custom Barcode Handling",
    "version": "1.0",
    "summary": "Custom Barcode Handling for Sales and Purchase Orders",
    "category": "Sales/Purchase",
    "author": "Amit Gangani",
    "depends": ["sale_management", "purchase", "barcodes"],
    "data": [
    ],
    "assets": {
        "web.assets_backend": [
            "custom_barcode_handling/static/src/**/*",
        ],
        "web.assets_unit_tests": [
            "custom_barcode_handling/static/tests/**/*",
        ],
    },
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
