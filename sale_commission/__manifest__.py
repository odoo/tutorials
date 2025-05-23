# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sale Commission",
    'version': '1.0',
    'depends': ['sale_management', 'sale_loyalty'],
    'author': "Raj Pavara",
    'description': """
    Sale Commission Application
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/commission_rule_views.xml',
        'views/commission_list_views.xml',
        'views/sale_order_menus.xml',
    ],
    'demo': [
    ]
}
