{
    "name": "POS Customer Display",
    "version": "1.0",
    "author": "Ravij Parikh (snrav)",
    "description": "Display customer name, amount/guest and refund lines in POS",
    "depends": ["point_of_sale"],
    "application": True,
    "license": "LGPL-3",
    "assets": {
        "point_of_sale.assets": [
            "pos_customer_display/static/src/pos_order.js",
        ],
        "point_of_sale.customer_display_assets": [
            "pos_customer_display/static/src/customer_display/*",
        ],
    }
}
