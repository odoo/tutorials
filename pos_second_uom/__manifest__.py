{
    "name": "POS Second UoM",
    "description": """
    This module allows cashier to sell product in second unit of measure
    """,
    "depends": [
        "product",
        "point_of_sale",
    ],
    "data": ["views/product_template.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_second_uom/static/src/**/*",
        ]
    },
    "license": "LGPL-3",
    "application": True,
    "installable": True,
}
