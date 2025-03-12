{
    'name': 'POS Salesperson',
    'version': '1.0',
    'description': 'Add POS salesperson',
    'depends': ["point_of_sale"],
    'data': [
        # "views/pos_salesperson_views.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*'
        ]
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
