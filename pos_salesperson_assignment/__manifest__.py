{
    'name': "POS Salesperson Assignment",
    'description': """
    Able to select salesperson(employee) on POS (billing screen).
    """,
    'version': '1.0',
    'depends': ['point_of_sale', 'pos_hr'],
    'author': "Prince Beladiya",
    'license': 'LGPL-3',
    'installable': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson_assignment/static/src/**/*',
        ],
    },
    'data': [
        'views/pos_order_view.xml'
    ]
}
