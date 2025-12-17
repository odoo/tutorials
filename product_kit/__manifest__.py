{
    'name': "Product As Kit",
    'version': '1.0',
    'depends': ['stock', 'sale_management'],
    'author': "Rishav Shah",
    'category': 'product',
    'description': """
    Add new new product type as kit
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/kit_products_wizard_views.xml',
        'views/sale_order_report.xml',
        'views/invoice_report.xml',
    ],
}
