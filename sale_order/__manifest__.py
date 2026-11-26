{
    'name': "sale_order",
    'summary': "prevent to create sale_order if there is available stock is NILL",
    'author': "Hansil",
    'category': 'Sales/Sales',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
}
