{
    "name": "POS second UOM",
    "version": "1.0",
    "depends": ["base", "point_of_sale", "web"],
    "category": "Sales/Point of Sale",
    "data": ["views/product_view.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_second_uom/static/src/**/",
        ],
    },
    "sequence": 1,
    "application": True,
    "license": "OEEL-1",
}
