{
    "name": "Sale enhancements",
    "version": "1.0",
    "description": 
    """
    SHOW LAST ORDERED PRODUCTS FOR CUSTOMERS IN SALE ORDER AND PURCHASE ORDER
    """,
    "depends": ["sale_management","product","stock","purchase"],
    "data": [
        "views/product_views.xml",
        "views/account_move_views.xml",
    ],
        "application": True,
        "license": "LGPL-3",
    "assets" : {
        "web.assets_backend": [
            "sale_enhancements/static/src/product_catalog/kanban_model.js",
            "sale_enhancements/static/src/product_catalog/product_catalog.js",
        ],
    },
}
