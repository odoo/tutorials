{
    'name': 'Rental Deposit',
    'version': '1.0',
    'depends': ['sale_renting', 'website_sale'],
    'category': 'Sales',
    'Summary': 'Add deposit logic to rental products on sale order and webshop',
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/product_webiste_template_views.xml',
        ],
        'assets': {
        'web.assets_frontend': {
            'deposit_rental/static/src/website_deposit_amount.js',
        }
    },
    'license': 'LGPL-3',
}
