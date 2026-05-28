{
    "name": "Website_sale/Sale_renting_deposit Bridge",
    "application": False,
    "installable": True,
    "author": "sngoh",
    "depends": ["website_sale", "sale_renting_deposit", "website_sale_renting"],
    "auto_install": True,
    "license": "LGPL-3",
    "category": "Sale",
    "data": [
        "views/template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_sale_renting_deposit_bridge/static/src/js/variant_configurator.js"
        ],
    },
}
