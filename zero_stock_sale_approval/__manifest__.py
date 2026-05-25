{
    'name': 'Sale Zero Stock Approval',
    'description': 'Grant permission to confirm approved orders without stock.',
    'depends': ['sale_management', 'sale_stock'],
    'author': 'moahi',
    'license': 'LGPL-3',
    'data': [
        'views/sale_order_views.xml',
    ]
}
