{
    'name': "product_kit",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'author': "Kalpan Desai",
    'category': 'Sales/Sales',
    'description': """
        Module specifically designed to manage product as kits in Odoo.
    """,
    'installable': True,
    'application': True,
    'data': [
        'views/product_views.xml',
        'wizards/sub_product_wizard_view.xml',
        'views/sale_order_view.xml',
        'views/sale_portal_view.xml',
        'security/ir.model.access.csv',
    ],
}
