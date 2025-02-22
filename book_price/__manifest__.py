{
    'name': 'Pricelist Book Price',
    'version': '1.0',
    'author': 'Khushi',
    'summary': 'Added Book Price',
    'depends': ['sale_management'],
    'data' : [
        'views/account_move_line_views.xml',
        'views/sale_order_line_views.xml'
    ],
    'installable' :True,
    'auto_install':True,
    'application': False,
    'license': 'LGPL-3',
}
