# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Self Order Product Details",
    'category': 'Sales/Point Of Sale',
    'description': """
Open custom dialog on product click
""",
    'depends': ['pos_self_order'],
    'assets': {
        'pos_self_order.assets': [
            'odoo_self_order_details/static/src/**/*'
        ],
    },
    'installable': True,
    'application': True,
    'license': "LGPL-3",
}
