{
    "name": "POS Second UoM",
    "category": "Point of Sale",
    "depends": ["product", "uom", "point_of_sale"],
    "author": "habar",
    "data": [
        "views/product_template_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_second_uom/static/src/js/control_buttons.js",
            "pos_second_uom/static/src/xml/control_button.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
