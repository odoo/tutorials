{
    'author': 'Odoo S.A.',
    'name': 'Purchase Discount',
    'depends': ['purchase'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_discount_views.xml',
        'views/purchase_order_views.xml'
    ],
    'application': True,
    'installable': True
}
