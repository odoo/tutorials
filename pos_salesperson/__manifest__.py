{
    'name': "POS Salesperson",
    'description': "This adds option to choose sales person on pos app.",
    'version': '1.0',
    'category': 'Tutorials',
    'installable': True,
    'depends': ['pos_hr'],
    'data': [
        "views/pos_order_views.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*',
        ],
    },
    'license': 'LGPL-3'
}
