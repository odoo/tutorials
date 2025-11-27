{
    "name": "Pick from Quant",
    "depends": ["stock_barcode"],
    "application": True,
    "data": [
        "views/stock_move_line_views_inherit.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'barcode_pick_quant/static/src/**/*.js',
        ]
    },
    'license': 'LGPL-3'
}
