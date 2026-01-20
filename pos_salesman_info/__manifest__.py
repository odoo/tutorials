{
    'name': "POS Salesman Info",
    'depends': ['point_of_sale','hr'],
    'auto_install':True,
    'data': [
        "views/pos_order_view_inherited.xml"
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesman_info/static/src/**/*'
        ]
    },
    'license': 'LGPL-3'
}
