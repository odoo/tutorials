{
    'name': "Product Kit",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "Harsh Chaudhari",
    'category': 'Product Kit',
    'description': """
    Product Kit description...
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_kit_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': False,
    'installable': True,
}
