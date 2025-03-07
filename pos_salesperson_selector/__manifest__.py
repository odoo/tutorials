{
    'name':'Pos Salesperson Selector',
    'depends' : ['point_of_sale','hr'],
    'data' :  [
        'views/pos_order_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson_selector/static/src/**/*',
        ],
    },
    "license": "LGPL-3",
}
