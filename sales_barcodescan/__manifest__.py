{
    "name": "SO/PO barcode scan",
    "version": "1.0",
    "summary": "Add products to PO/SO from catalog via barcode scanning.",
    "author": "prbo",
    "depends": ["sale_management", "product"],
    "license": "LGPL-3",
    "assets": {
    "web.assets_backend": [
        "sales_barcodescan/static/src/**/*",
        ],
    },
    "installable": True,
    "application": True,
}
