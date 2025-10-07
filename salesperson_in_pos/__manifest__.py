{
    'name': "Salesperson_Pos",
    'version': "1.0",
    'summary': "Add salesperson field in POS app",
    'description': "This module adds a button in the POS dashboard to assign a salesperson to respective orders.",
    'author': "Priyansi Borda",
    'depends': ['base', 'point_of_sale', 'hr'],
    'data': [
        "views/pos_view.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'salesperson_in_pos/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
