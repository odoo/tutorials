{
    'name': 'Zero Stock Blockage',
    'author': 'Odoo - utsav',
    'license': 'LGPL-3',
    'category': 'sale',
    'summary': 'Allows approval of zaro stock sales order',
    'depends': ['sale_management', 'stock'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
