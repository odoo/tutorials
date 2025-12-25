{
    'name': 'Put In Pack -Stock',
    'category': 'Stock/PutInPack2',
    'summary': 'Full Traceability Report Demo Data',
    'author': 'Odoo S.A.',
    'depends': ['stock','purchase'],
    'description': "Custom put in pack button for Inventory Transfer",
    'license': 'LGPL-3',
    'installable': True,
    'data': [
        'views/view_custom_put_in_pack.xml',
        'views/view_stock_move_put_in_pack.xml',
        'views/stock_move_views.xml',
        'views/stock_quant_views.xml',
    ]
}
