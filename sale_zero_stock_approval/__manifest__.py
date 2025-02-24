{
    'name': 'zero_stock_blockage',
    'author': 'Odoo - utsav',
    'licence': 'LGPL-3',
    'category': 'sale',
    'summary': 'Allows approval of zaro stock sales order',
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
