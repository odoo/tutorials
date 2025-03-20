{
    'name': "Custom MRP Modular Type",
    'version': "1.0",
    'category': "Manufacturing",
    'author': "Vaidik Gorasiya",
    'depends': ['sale_management', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'wizard/modular_type_wizard.xml',
        'views/sale_order_line_views.xml',
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'license': 'AGPL-3'
}
