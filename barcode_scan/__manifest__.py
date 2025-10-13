{
    'name': "Barcode Scanning In SO/PO",
    'version': '0.1',
    'summary': 'Adds barcode scanning capabilities to product catalog',
    'depends': ['sale_management', 'stock_barcode', 'purchase'],
    'application': True,
    'installable': True,
    "assets": {
        'web.assets_backend': [
            'barcode_scan/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
