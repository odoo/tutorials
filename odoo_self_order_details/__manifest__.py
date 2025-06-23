{
    "name": "Self Order Details",
    "description": """
        Self order details for products in POS
    """,
    "author": "Ayush Patel",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["pos_self_order"],
    "license": "LGPL-3",
    "assets": {
        "pos_self_order.assets": [
            "odoo_self_order_details/static/src/**/*",
        ],
    },
    "data": [
        "views/product_template_view.xml",
    ],
}
