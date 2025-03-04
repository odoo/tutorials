{
    "name": "deposit_rental",
    "description": "An extension module which helps to implement the deposit option in the rental app",
    "summary": "Adding deposit feature in Rental App",
    "version": "1.0",
    "author": "Vedant Pandey (vpan)",
    "depends": ["sale_renting", "website_sale"],
    "data": [
        "views/product_template_views.xml",
        "views/res_config_settings_view_form.xml",
        "views/website_sale.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            'deposit_rental/static/src/**/*',
        ],
    },
    "license": "OEEL-1",
    "installable": True
}
