{
    'name': "POS Salesperson",
    'summary': 'Adds a salesperson selection button in POS.',
    'version': '0.1',
    'author': 'Sudhirkumar Sharma',
    'website': 'https://www.odoo.com',
    'category': 'Sales',
    'depends':['point_of_sale', 'hr'],
    'data':[
        'views/pos_order_views.xml',
    ],
    'assets':{
        "point_of_sale._assets_pos":[
            'pos_salesperson/static/src/**/*',
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
