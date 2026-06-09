{
    'name': 'POS Second UoM',
    'author': 'Aditi (adpaw)',
    'category': 'Point of Sale',
    'summary': 'Allow cashier to enter quantity using a second UOM in POS',
    'depends': ['point_of_sale'],
    'license': 'LGPL-3',
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_second_uom/static/src/second_uom_popup/second_uom_popup.xml',
            'pos_second_uom/static/src/second_uom_button/second_uom_button.xml',
            'pos_second_uom/static/src/second_uom_popup/second_uom_popup.js',
            'pos_second_uom/static/src/second_uom_button/second_uom_button.js',
        ],
    },
    'installable': True,
    'auto_install': True,
}
