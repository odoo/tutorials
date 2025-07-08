{
    'name': "Barcode Scanning In SO/PO",
    'category': '',
    'version': '0.1',
    'depends': ['product', 'barcodes', 'sale', 'web', 'stock_barcode', 'purchase'],
    'sequence': 1,
    'application': True,
    'installable': True,
    "assets": {
        'web.assets_backend': [
            'barcode_scan/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
