{
    "name": "Rental Deposit Feature",
    "version": "1.0",
    "summary": "Adds deposit for rental products.",
    "author": "Odoo PS",
    "category": "Sales/Rental",
    "depends": ["sale_renting", "sale_management", "website_sale"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
