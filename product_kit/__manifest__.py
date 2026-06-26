{
    'name': 'Product Kit',
    'version': '1.0',
    'depends': ['base', 'sale', 'product', 'stock'],
    'application': True,
    'installable': True,
    'author': "odoo s.a",
    'category': 'Tutorials',
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/kit_config_wizard_views.xml',
    ],
}
