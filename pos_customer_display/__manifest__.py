{
    "name": "POS customer display",
    "author": "Harsh Siddhapara siha",
    "version": "1.0",
    "depends": ["pos_restaurant"],
    "assets": {
        "point_of_sale.assets_prod": [
            "pos_customer_display/static/src/pos_order.js",
        ],
        "point_of_sale.customer_display_assets": [
            "pos_customer_display/static/src/customer_display/**/*",
        ],
    },
    "installble": True,
    "license": "LGPL-3",
}
