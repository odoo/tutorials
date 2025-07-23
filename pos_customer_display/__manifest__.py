{
    "name": "POS Customer Display",
    "author": "Dhruvrajsinh Zala (zadh)",
    "summary": "Display Customer Info, Amount Per Guest, and Segregated Refunds in POS",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "installble": True,
    "license": "LGPL-3",
    "assets": {
        "point_of_sale.assets_prod": [
            "pos_customer_display/static/src/pos_order.js",
        ],
        "point_of_sale.customer_display_assets": [
            "pos_customer_display/static/src/customer_display/**/*",
        ],
    }
}
