{
    "name": "Sale Person In Pos",
    "depends": ["point_of_sale", "hr"],
    "data": [
        "views/pos_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "sales_person_in_pos/static/src/**/*",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
