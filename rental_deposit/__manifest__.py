{
    'name': 'Rental deposit',
    'author': "keman",
    'license': 'LGPL-3',
    'depends': ['sale_renting', 'website_sale'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_template_views.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'rental_deposit/static/src/js/deposit.js',
        ],
    },
}
