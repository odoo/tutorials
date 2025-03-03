{
    'name': "POS salesperson",
    'version': '1.0',
    'depends': ['point_of_sale', 'hr'],
    'author': "djsh",
    'category': '',
    'description': """
POS salesperson assignment functionality.
""",
    'data': [
        'views/pos_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson_assign/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}
