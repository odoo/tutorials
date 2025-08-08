{
    'name': 'Pos Salesperson',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Allow selecting salesperson for pos order',
    'depends': ['point_of_sale', 'hr'],
    'installable': True,
    'data': [
        'views/pos_order_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
