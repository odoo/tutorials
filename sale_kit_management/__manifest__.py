{
    'name': 'Sale Kit Management',
    'version': "1.0",
    'category': "Sales/Sales",
    'description': "Creates a Kit Option in Products and Sales Order",
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_kit_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'author': "times",
    'license': "LGPL-3",
}
