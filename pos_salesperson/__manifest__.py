{
    'name': "POS salesperson",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['pos_hr'],
    'author': "Kalpan Desai",
    'category': 'Sales/Point of Sale',
    'description': """
    Salesperson in POS
    """,
    'installable': True,
    'application': True,
    'data': [
        'views/pos_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*'
        ]
    },
}
