{
    'name': "Last Ordered Products (Stock)",
    'version': '1.0',
    'depends': ['last_ordered_products', 'stock', 'sale_management', 'purchase'],
    'author': "Parthav Chodvadiya (PPCH)",
    'category': '',
    'description': """
    Show On hand quantity in product catalog with + and - forecasted quantity
    """,
    'data': [
        'views/product_views.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': True,
}
