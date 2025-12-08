{
    'name': 'Sales Modular Products',
    'version': '1.0',
    'summary': 'Automate creation of modular product lines on sales orders.',
    'author': 'ksoz',
    'depends': ['sale_management', 'product', 'mrp'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizards/modular_wizard_views.xml',
        'views/modular_type_views.xml',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'views/sale_order_view.xml',
        'views/mrp_production_view.xml',
    ],
    'installable': True,
    'application': False,
}
