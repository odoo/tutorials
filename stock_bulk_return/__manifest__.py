# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Stock Bulk Return",
    'category': 'Inventory/Inventory',
    'summary': "Bulk return of products sold or purchased.",
    'description': """
Bulk return of products sold or purchased.
    """,
    'depends': ['purchase', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_bulk_return_views.xml',
        'views/stock_menu_views.xml',
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_bulk_return/static/src/js/tours/**/*',
        ],
    },
    'application': False,
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
