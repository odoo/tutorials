# -*- coding: utf-8 -*-

{
    'name': 'Rental Deposit',
    'version': '1.0',
    'category': 'Sales/Rental',
    'summary': 'Add deposit functionality to rental products',
    'author': 'Maan Patel',
    'description': """
        This module adds the ability to require deposits for rental products.
        A deposit can be configured for each rental product and will be automatically
        added to the sales order when the product is rented.
    """,
    'depends': ['sale_management', 'website_sale_renting'],
    'data': [
        'views/res_config_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_templates.xml'
    ],
    'assets': {
        'web.assets_frontend': ['rental_deposit/static/src/js/website_sale_renting.js'],
    },
    'installable': True,
    'license': 'LGPL-3'
}
