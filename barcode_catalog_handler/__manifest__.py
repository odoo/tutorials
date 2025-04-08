{
    'name': "Barcode Catalog Handler",
    'version': "1.0",
    'summary': """This module used to scans barcodes in product catalog kanban to add/increase quantity in Sale/Purchase Orders.""",
    'depends': [
        "barcodes",
    ],
    'assets': {
        "web.assets_backend": [
            "barcode_catalog_handler/static/src/product_catalog/*"
        ],
        "web.assets_unit_tests": [
            "barcode_catalog_handler/static/tests/**/*"
        ],
    },
    'license': "LGPL-3",
    'auto_install': True,
    'application': False,
    'installable': True,
}
