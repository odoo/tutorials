{
    'name': 'POS Salesperson',
    "author": "Shiv Bhadaniya",
    'summary': 'Adds a salesperson',
    'category': 'Point of Sale',
    'depends': ['point_of_sale', 'hr'],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_salesperson/static/src/**/*",
        ],
    },
    "data": [
        "views/pos_order_views.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
