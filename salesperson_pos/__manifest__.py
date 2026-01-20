{
    "name": "SalesPerson Choosing Button In Pos",
    "version": "1.0",
    "depends": ["point_of_sale", "hr"],
    "data": ["views/pos_order_views.xml"],
    "appication": True,
    "installable": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "salesperson_pos/static/src/**/*",
        ],
    },
    "license": "LGPL-3",
}
