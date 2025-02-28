{
    'name': "POS Salesperson",
    'summary': 'Adds a salesperson selection button in POS.',
    'version': '0.1',
    'author': 'Sudhirkumar Sharma',
    'website': 'https://www.odoo.com',
    'category': 'Sales',
    'depends':[
        'point_of_sale',
        'hr',
    ],
    'data':[
        'views/pos_order_views.xml',
    ],
    'assets':{
        "point_of_sale._assets_pos":[
            'pos_salesperson/static/src/models/pos_order.js',
            'pos_salesperson/static/src/select_salesperson_button/select_salesperson_button.js',
            'pos_salesperson/static/src/select_salesperson_button/select_salesperson_button.xml',
            'pos_salesperson/static/src/control_button/control_button.js',
            'pos_salesperson/static/src/control_button/control_button.xml',
        ]
    },
    'installable': True,
    'application': False,
    'lisence': 'LGPL-3',
}
