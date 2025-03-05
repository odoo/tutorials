{
    'name': "Rental Deposit Feature",
    'version': "1.0",
    'summary': "Adds deposit functionality for rental products.",
    'author': "Harsh Shah (hash)",
    'category': "Sales/Rental",
    'depends': ["sale_management", "website_sale_renting"],
    'data': [
        "views/res_config_settings_view.xml",
        "views/product_template_view.xml",
        "views/website_sale_view.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sale_renting_deposit/static/src/**/*',
        ],
    },
    'installable': True,
    'license': "LGPL-3"
}
