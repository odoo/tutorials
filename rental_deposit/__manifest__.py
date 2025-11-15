{
    "name": "rental_deposit",
    "version": "1.0",
    "author": "ksni-odoo",
    "depends": ["sale_renting", "website", "website_sale"],
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/product_view_template.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "rental_deposit/static/src/js/website_sale.js"
        ]
    }
}
