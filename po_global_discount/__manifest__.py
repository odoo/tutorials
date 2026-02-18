{
    'name': 'Purchase global discount',
    'version': '0.1.0',
    'description': 'Add a global discount to the all purchase order lines',
    'depends': [
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'wizard/purchase_global_discount_view.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Ishwar',
    'license': 'LGPL-3'
}
