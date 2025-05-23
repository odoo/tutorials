# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Rental Deposit",
    'category': 'Sales',
    'summary': "Automatically add a deposit amount to rental orders.",
    'description': """
This module adds a deposit amount automatically when renting a product which requires deposit.
The deposit amount is automatically applied based on the configured deposit product and the rented product quantity.
Ideal for businesses that require a refundable security deposit on rental items.
    """,
    'depends': ['sale_renting', 'website_sale'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/sale_renting_deposit_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sale_renting_deposit/static/src/**/*',
        ],
    },
    'application': False,
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
