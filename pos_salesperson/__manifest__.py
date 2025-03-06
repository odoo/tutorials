{
    'name': "POS Salesperson",
    "author": "Lucky Prajapati",
    'summary': 'Adds a salesperson dropdown to the POS screen',
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
    'license': 'AGPL-3'
}
