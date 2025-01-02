{
    'name': 'product_warranty',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'description': 'Enable user to add warranty for product in SO',
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',

        'wizard/warranty_wizard.xml',

        'views/product_template_views.xml',
        'views/warranty_configuration_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3', 
}
