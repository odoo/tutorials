{
    'name': 'Deposit Rental',
    'description': 'Adds deposit functionality for rental products.',
    'category': 'Rental/Deposit',
    'depends': [
        'sale_renting',
        'website_sale'
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_rental_templates.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
