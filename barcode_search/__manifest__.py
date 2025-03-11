{
    'name': 'Barcode Search For PO/SO',
    'description': 'Allows to search product by barcode in Purchase Order and Sales Order',
    'depends': ['sale', 'sale_management', 'barcodes'],
    'data': [
        "views/product_template_kanban_view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'barcode_search/static/src/js/sale_order_catalog_service.js',
            'barcode_search/static/src/js/product_data_load.js',
            'barcode_search/static/src/js/kanban_record.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}

