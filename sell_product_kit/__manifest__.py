{
    'name': 'Sell Product Kit',
    'description': "Module to add function to sell product as a kit.",
    'installable': True,
    'application': False,
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_kit_view_form.xml',
        'views/sale_order_view.xml'
    ],
    'license':'LGPL-3'
}
