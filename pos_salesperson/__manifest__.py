{
    'name': "POS Salesperson",
    'version': '1.0',
    'category': 'Point of Sale',
    'author': "Odoo S.A.",
    'depends': ['pos_hr'],
    'data':[
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**',
        ],
    },
    'installable': True,
    'license': 'LGPL-3'
}
