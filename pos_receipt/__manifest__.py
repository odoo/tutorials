{
    "name": "POS Receipt",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/custom_lined_layout.xml",
        "views/custom_boxes_layout.xml",
        "views/custom_light_layout.xml",
        "views/pos_reciept_views.xml",
        "wizard/pos_receipt_layout.xml",
    ],
    "assets": {"point_of_sale._assets_pos": ["pos_receipt/static/src/**/*"]},
    "license": "LGPL-3",
}
