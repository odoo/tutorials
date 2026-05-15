{
    'name': 'Renting Deposit',
    'author': "Ayush Khubchandani (aykhu)",
    'license': 'LGPL-3',
    'depends': ['sale_renting', 'website_sale'],
    'data': [
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
        'views/website_sale_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sale_renting_deposit/static/src/js/deposit_rental.js',
        ],
    },
}
