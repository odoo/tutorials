{
    'name': 'modular Types',
    'version': '1.0',
    'summary': 'Add modular types to products and set price of MO lines according to modular types',
    'author': 'chirag Gami(chga)',
    'category': 'Manufacture',
    'depends': ['base', 'sale_management', 'mrp'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/mrp_bom_views.xml',
        'views/sale_order_views.xml',
        'wizard/modular_type_wizard_views.xml',
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'application': True,
}
