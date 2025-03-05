{
    'name': "Kit Product Type",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "Prince Beladiya",
    'description': """
    To add a new product type - kit
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/product_type_kit_wizard_views.xml',
    ],
}
