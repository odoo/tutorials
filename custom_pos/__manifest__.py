{
    'name': 'custom_pos',
    'description': 'A customized pos app designed to sell products at their custom price and restrict salesperson to sell it below its min price also this customization helps us to search sales order from product barcode in the refund screen',
    'summary': 'Customized POS solution providing custom price functionality with barcode search refund',
    'version': '1.0',
    'author': 'Vedant Pandey (vpan)',
    'depends': ['point_of_sale'],
    'data': [
        'views/product_template_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'custom_pos/static/src/app/models/product_product.js',
            'custom_pos/static/src/app/models/pos_order_line.js',
            'custom_pos/static/src/app/generic_components/orderline/**/*',
            'custom_pos/static/src/app/screens/ticket_screen/**/*',
            'custom_pos/static/src/app/generic_components/order_widget/**/*',
        ],
        'web.assets_tests':[
            'custom_pos/static/tests/tours/ticket_screen_tour.js',
            'custom_pos/static/tests/tours/order_widget_tour.js'
        ]
    },
    'license': 'LGPL-3',
    'installable': True,
}
