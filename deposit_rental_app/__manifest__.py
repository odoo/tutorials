{
    "name": "Deposit In Rental App",
    "author": "Krishna Patel",
    "depends": ["sale_renting","website","website_sale"],
    "data": [
        "views/product_template_views.xml",
        "views/website_sale_product.xml",
        "views/res_config_settings.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'deposit_rental_app/static/src/js/quantity_update.js',
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}   
