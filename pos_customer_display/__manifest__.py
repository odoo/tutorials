{
    "name": "POS Customer Display",
    "version": "1.0",
    "summary": """Improve customer's display to show customer name, amount, number of guest and segregate refund section""",
    "depends": ["base", "point_of_sale"],
    "category": "Point of Sale",
    "assets": {
        "point_of_sale.customer_display_assets": [
            "pos_customer_display/static/src/js/customer_display_extend.xml"
        ],
        "point_of_sale.assets_prod": [
            "pos_customer_display/static/src/js/customer_display_extend.js"
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
