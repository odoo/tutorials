{
    'name': "sub_product",
    'depends': ['sale_management'],
    'author': "sahm@odoo.com",
    'description': "This module will help to add sub-product in product.",
    'data': [
        'security/ir.model.access.csv',
        'wizard/sub_products_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml'
    ],
    'demo': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
