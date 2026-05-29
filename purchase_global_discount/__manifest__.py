{
    'name': 'Purchase Order Global Discount',
    'version': "1.0",
    'category': "Supply Chain/Purchase",
    'description': "Creates a Discount Option in Purchase Order",
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_order_discount_views.xml',
        'views/purchase_views.xml',
    ],
    'auto_install': True,
    'author': "times",
    'license': "LGPL-3",
}
