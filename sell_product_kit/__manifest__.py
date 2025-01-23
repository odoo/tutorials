{
    'name': 'Sell Product Kit',
    'description': "Module to add function to sell product as a kit.",
    'installable': True,
    'application': False,
    'depends': ['product', 'sale','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_kit_view_form.xml',
        'views/new_product_kit_view.xml',
        'wizard/product_sub_product_wizard.xml',
        'views/sale_order_view.xml',
    ],
    'license':'LGPL-3'
}
