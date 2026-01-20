{
    'name': "Salesperson in Pos",
    'description': """
        This custom module add salesperson on the POS screen during the billing process
    """,
    'author': "Dhruv Godhani",
    'installable': True,
    'depends': ['point_of_sale','hr'],
    'data': [
        "views/pos_order_view.xml"
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'salesperson_pos/static/src/**/*'
        ]
    },
    'license': 'LGPL-3',
}
