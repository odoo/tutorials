{
    "name": "Website Product Quotation",
    "category": "Website/Website",
    "description": "A website page to display set of products",
    "author": "Darpan",
    "depends": ["website", "website_sale", "crm"],
    "application": True,
    "installable": True,
    "auto_install": ["website"],
    "data": [
        "demo/product_attributes_demo.xml",
        "demo/product_demo.xml",
        "views/product_quote_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_product_quotation/static/src/scss/product_quote_template.scss",
            "website_product_quotation/static/src/interactions/product_quote.js",
        ]
    },
    "license": "AGPL-3",
}
