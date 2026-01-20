{
    'name': 'Product Kit',
    'sequence': 1,
    'category': 'Tutorials/product_kit',
    'version': '1.0',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'sale_management',
        'account'
    ],
    'data': [
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/kit_products_wizard_views.xml',
        'security/ir.model.access.csv',
        'views/sale_order_report.xml',
        'views/account_move_views.xml',
    ]
}
