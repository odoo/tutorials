{
    "name": "Pos Salesperson",
    "depends": ["pos_hr"],
    "version": "0.1",
    "license": "LGPL-3",
    "installable": True,
    "data": ["views/pos_order_views.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/app/**/*"
        ]
    }
}
