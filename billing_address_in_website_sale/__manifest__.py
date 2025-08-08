{
    "name": "Billing Address In Website",
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "billing_address_in_website_sale/static/src/**/*",
        ],
        "web.assets_tests": [
            "billing_address_in_website_sale/static/tests/**/*",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
