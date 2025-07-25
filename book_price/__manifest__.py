# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Book Order Price',
    'version': '1.0',
    'depends': ['account', 'sale'],
    'author': 'Odoo',
    'website': 'https://www.odoo.com/',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'description': '''
    Book Order Price
    ''',
    'data': [
        'views/account_move_line_views.xml',
        'views/sale_order_line_views.xml'
    ],
}
