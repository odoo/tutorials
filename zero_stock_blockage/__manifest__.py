{
    'name': 'Zero Stock Blockage',
    'version': '1.0',
    'summary': 'Restricts sales order confirmation without Zero Stock Approval',
    'depends': ['sale_management','sales_team'],
    'license': "LGPL-3",
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
