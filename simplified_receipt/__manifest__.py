{
    "name": "POS Simplified Receipt",
    "summary": "",
    "description": """  """,
    "depends": ["point_of_sale" , "pos_restaurant"],
     "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "simplified_receipt/static/src/**/*",
        ],
    },
    "auto_install": True,
    "license": "LGPL-3",
}
