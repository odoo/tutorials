{
    'name': 'Adding Warranty',
    'version': '1.0',
    'depends': ['base', 'website_sale', 'product', 'stock', 'sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/warranty_configuration_views.xml',
        'wizard/product_display_wizard_views.xml',
        'views/add_warranty_button_views.xml',
        'views/warranty_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
