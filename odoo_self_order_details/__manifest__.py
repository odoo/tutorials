{
    "name": "Odoo self order details",
    "version": "1.0",
    "depends": ["base", "pos_self_order"],
    "license": "LGPL-3",
    "assets": {
        "pos_self_order.assets": [
            "odoo_self_order_details/static/src/**/*",
        ],
    },
    "data": [
        "views/product_template_view.xml",
    ],
    "installable": True,
    "application": True,
}
