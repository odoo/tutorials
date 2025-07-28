{
    'name': 'Rental Deposit',
    'version': '1.0',
    'category': 'Rental',
    'author': 'rodh',
    'license': "LGPL-3",
    'summary': 'Add deposit product functionality for rentals',
    'depends': ['sale_renting', 'website_sale'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_product.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
