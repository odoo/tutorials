{
    "name": "Last Purchased Products",
    "version": "1.0",
    "depends": ["sale_management", "purchase", "stock"],
    "author": "danal",
    "category": "Category",
    "license": "LGPL-3",
    "data": [
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/purchase_order_views.xml",
        "views/product_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "last_purchased_products/static/src/product_catalog/**/*.xml",
        ]
    },
    "installable": True,
    "application": False,
}
