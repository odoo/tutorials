{
    'name': 'Product Type Kit',
    'version': '1.0',
    'category': 'Sales',
    'license': 'LGPL-3',
    'summary': 'Custom product kit functionality without using BoM',
    'depends': ['sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/kit_subproduct_wizards.xml',
    ],
    'installable': True,
    'application': True,
}
