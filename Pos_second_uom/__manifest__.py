{
    'name': 'Pos_second_uom',
    'version': '1.0',
    'depends': ['point_of_sale', 'product'],
    'category': 'Point of Sale',
    'summary': 'Sell products using a second unit of measure in POS',
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'Pos_second_uom/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': True,
    'application': True,
}
