{
    'name': 'POS Add Salesperson',
    'version': '1.0',
    'category': 'Point of Sale',
    'depends': ['point_of_sale', 'hr'],
    'data':[
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**',
        ],
    },
    'installable': True,
    'application': False,
}