{
    "name": "POS Receipt Customization",
    "summary": "Customizable POS receipt with layouts and HTML header/footer",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "author": "Rohit",
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/receipts_layout_view.xml",
        "views/pos_retail_receipt_template.xml",
        "views/pos_restaurant_receipt_template.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_reciept_customize/static/src/**/*",
        ]
    },
    "auto_install": True,
}
