{
    "name": "Rental Deposit",
    "category": "Sales",
    "depends": ["sale_renting", "website_sale"],
    "Summary": "Add deposit logic to rental products on sale order and webshop",
    "installable": True,
    "data": [
        "views/res_config_settings_views.xml",
        "views/products_template_views.xml",
        "views/product_webiste_template_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "rental/static/src/website_deposit_amount.js",
        ]
    },
    "license": "AGPL-3",
}
