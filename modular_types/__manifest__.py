{
    'name': 'Modular Types',
    'version': '1.0',
    'category': 'Manufacturing',
    'author': 'haman',
    'depends': ['product', 'mrp', 'sale_management'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/mrp_bom_views.xml',
        'views/sale_order_views.xml',
        'views/mrp_modular_views.xml',
        'wizard/modular_type_wizard_views.xml',
    ],
    'installable': True,
}
