{
    'name': 'product warranty',
    'version': '1.0',
    'summary': 'adding product warranty',
    'author': 'abpa',
    'license': 'LGPL-3',
    'depends': ['product', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/warranty_wizard_views.xml',
        'views/warranty_configuration_views.xml',
        'views/product_template_views.xml',
        'views/add_warranty_button.xml',
        'views/warranty_menus.xml'
    ],
    'installable': True,
    'application': True,
}
