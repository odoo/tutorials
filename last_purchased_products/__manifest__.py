{
    "name": "Last Purchased Products",
    "description": """
    add last order time next to product display name,
    order product list as recently to old invoice creation time,
    add same functionality to customer invoice,
    add Unit of Measure next to price in catalog kanban view,
    add recent invoice time after price in catalog kanban view,
    add customer name next to invoice time.
    """,
    "version": "1.0",
    "depends": ["sale_management", "purchase", "stock"],
    "author": "danal",
    "category": "Category",
    "license": "LGPL-3",
    "data": [
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/purchase_order_views.xml",
        "views/product_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "last_purchased_products/static/src/product_catalog/**/*.xml",
        ]
    },
    "installable": True,
    "application": False,
}
