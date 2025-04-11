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
    'point_of_sale.assets': [
        'Pos_second_uom/static/src/js/add_quantity_button.js',
        'Pos_second_uom/static/src/xml/add_quantity_button.xml',
    ],
},

    'installable': True,
    'auto_install': True,
    'application': True,
}
