{
    'name': 'Multi Warehouse Sale Order',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Enable multi-warehouse delivery',
    'depends': ['sale_management', 'stock'],
    'license': 'LGPL-3',
    'author': 'Shiv Bhadaniya (sbha)',
    'data': [
        'views/product_template_views.xml',
        'views/sale_order_line_views.xml',
        'views/multi_warehouse_menus.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'multi_warehouse_sale_order/static/src/**/*',
        ],
    },
}
