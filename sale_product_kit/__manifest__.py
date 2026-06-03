{
    'name': 'Product Kit',
    'author': 'Ayush Khubchandani (aykhu)',
    'license': 'LGPL-3',
    'depends': ["sale", "product"],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'wizard/product_kit_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sale_product_kit/static/src/js/product_kit_sale_order_line.js',
        ],
    },
}
