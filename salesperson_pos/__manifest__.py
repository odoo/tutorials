# -*- coding: utf-8 -*-
{
    'name': 'salesperson_pos',
    'summary': 'Adding salesperson in the POS Screen',
    'author': 'Odoo',
    'website': 'https://www.odoo.com',
    'category': 'POS',
    'version': '0.1',
    'depends': ['point_of_sale', 'pos_hr'],
    'data': [
        'views/pos_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'salesperson_pos/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}

