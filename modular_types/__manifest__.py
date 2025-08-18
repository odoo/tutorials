{
    'name': 'Modular Types',
    'version': '1.0',
    'depends': ['base', 'sale_management', 'mrp', 'stock'],
    'author': 'Aryan Donga (ardo)',
    'description': 'Modular Types for BOM Components',
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_modular_type_views.xml',
        'views/mrp_bom_views.xml',
        'views/product_template_views.xml',
        'views/mrp_production_views.xml',
        'wizard/sale_order_line_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
}
