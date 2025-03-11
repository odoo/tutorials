{
    "name": "pos_salesperson",
    "version": "1.0",
    "author": "ksni-odoo",
    "depends": ["point_of_sale", "hr"],
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "views/pos_order_view.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/**/*"
        ]
    }
}
