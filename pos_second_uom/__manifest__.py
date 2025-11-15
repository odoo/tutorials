{
    'name': 'Add Second UOM in POS',
    'version': '1.0.0',
    'category': 'Sales/Point of Sale',
    'depends': ['point_of_sale'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data':[
        "views/product_template_views_inherit.xml"
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_second_uom/static/src/**/*.js",
            "pos_second_uom/static/src/**/*.xml",
        ],
    },
}
