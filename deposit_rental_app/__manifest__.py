{
    "name": "Deposit Rental App",
    "description": """
Adds a deposit to a rental product on the webshop
    """,
    "category": "Sales/Sales",
    "depends": ["account", "sale_renting", "website_sale"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "deposit_rental_app/static/src/js/sale_product_field.js",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
