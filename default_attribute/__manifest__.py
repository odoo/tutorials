{
    'name': "Default Attribute Product Configurator",
    'version': '1.0',
    'depends': [ 'accountant', 'sale_management', 'stock'],
    'author': "djsh",
    'category': '',
    'description': """
Default attribute for configuration of products.
""",
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/global_info_attributes_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
