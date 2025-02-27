{
    'name': 'POS Second Unit of Measure',
    'depends': ['point_of_sale', 'uom'],
    'data': [
        'views/product_template_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_uom_extension/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
