{
    "name": "Deposit Rental",
    "description": "Adds deposit functionality for rental products.",
    "category": "Rental/Deposit",
    "depends": ["sale_renting","website_sale"],
    "data": [
        "views/website_sale_templates.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
