{
    'name': "Warranty",
    'depends': ['sale_management'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/warranty_configuration_views.xml',
        'wizard/warranty_wizard.xml',
        'views/sale_order_views.xml',
        'data/warranty_configuration_data.xml',
    ]
}
