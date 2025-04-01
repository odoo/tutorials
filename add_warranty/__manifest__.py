{
    'name': 'Add Warranty',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/warranty_wizard_views.xml',
        'views/product_template_views.xml',
        'views/warranty_configuration_views.xml',
        'views/sales_order_views.xml',
        'views/warranty_menus.xml',
    ]
}
