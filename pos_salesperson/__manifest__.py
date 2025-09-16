{
    "name": "POS - Salesperson",
    "version": "1.0",
    "description": """
This Module provides Salesperson choosing button in POS.
    """,
    "category": "Point of Sale",
    "depends": ["point_of_sale", "hr"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/**",
        ],
    },
    "data": [
        "views/pos_order_view.xml",
    ],
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
