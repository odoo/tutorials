{
    'name': 'Modular Types',
    'version': '1.0',
    'author': 'Kartavya Desai (kade)',
    'description': 'Enables modular types feature',
    'depends': [
        'sale_management',
        'mrp',
    ],
    'data':[
        'security/ir.model.access.csv',
        'wizards/modular_types_wizard_views.xml',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'views/sale_order_line_views.xml',
        'views/stock_move_views.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
}
