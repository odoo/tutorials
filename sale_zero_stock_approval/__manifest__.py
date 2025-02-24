{
    'name': 'Sale Zero Stock Approval',
    'version': '1.0',
    'summary': 'Allows approval of zero stock sales orders',
    'author': 'smjo-odoo',
    'depends': ['sale_management', 'stock'],
    'data': ['views/sale_order_view.xml',],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3'
}
