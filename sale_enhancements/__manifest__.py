{
    "name": "Sale enhancements",
    "version": "1.0",
    "description": "ENHANCE SALE ORDER WITH NEW FEATURES",
    "depends": ["sale_management", "account","product","stock","purchase"],
    "data": [
        "views/product_views.xml"
    ],
    "assets" : {
        "web.assets_backend": [
            "sale_enhancements/static/src/product_catalog/kanban_model.js",
            "sale_enhancements/static/src/product_catalog/product_catalog.js",
        ],
    },
    "application": True,
    "license": "LGPL-3",
}
