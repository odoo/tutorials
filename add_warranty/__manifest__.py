{
    'name': 'Add Warranty',
    'version': '1.0',
    'author': 'Kartavya Desai (kade)',
    'description': 'Add feature of extended warranty.',
    'depends': [
        'sale_management'
    ],
    'data':[
        'security/ir.model.access.csv',
        'wizards/add_warranty_wizard_views.xml',
        'views/warranty_configuration_views.xml',
        'views/warranty_menu.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'data/product_demo.xml',
        'data/warranty.configuration.csv'
    ],
    'license': 'LGPL-3',
    'installable': True,
}
