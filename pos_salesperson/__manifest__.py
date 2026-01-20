{
    "name": "pos_salesperson",
    "depends": ["base", "hr", "point_of_sale"],
    "data": ["views/pos_order_view_inherit.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/app/**/*",
        ],
    },
    "license": "LGPL-3",
}
