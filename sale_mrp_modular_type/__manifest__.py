{
    'name': 'Modular Type',
    'description': """This module adds modular type to Manufacturing orders""",
    'author': 'aykhu',
    'license': 'LGPL-3',
    'depends': ['sale_management', 'sale_mrp'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/modular_type_wizard_views.xml',
        'views/modular_type_views.xml',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'views/sale_order_views.xml',
    ],
}
