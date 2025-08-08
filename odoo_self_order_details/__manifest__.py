# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Odoo Self Order Details",
    'version': '1.0',
    'depends': ['pos_self_order'],
    'author': "Raj Pavara",
    'description': """
Odoo Self Order Details.
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'pos_self_order.assets': [
            'odoo_self_order_details/static/src/**/*',
        ],
    },
    'data': [
        'views/product_template_views.xml',
    ],
    'demo': [
    ]
}
