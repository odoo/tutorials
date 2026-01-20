{
    'name': "POS SalesPerson",
    'summary': 'Add a salesperson button in POS for selecting salesperson.',
    'version': '0.1',
    'author': 'Krunal Gelot',
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
    'license': 'LGPL-3'
}
