# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Deposit Rental',
    'version': '1.0',
    'depends': ['sale_renting', 'website_sale'],
    'description': """
This module helps to implement the deposit option in the rental app.
""",
    'data': [
        'views/product_template_view.xml',
        'views/res_config_settings_view.xml',
        'views/website_deposit_amount_template.xml',
    ],
    'assets': {
        'web.assets_frontend': {
            'deposit_rental/static/src/website_deposit_amount.js',
        }
    },
    'license': 'LGPL-3'
}
