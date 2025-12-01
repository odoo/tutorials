{
    "name": "Point of Sale Salesperson",
    "description": """
    Point of Sale Salesperson Module to add Salesperson in pos order, form and billing in session.
    """,
    "version": "1.0",
    "depends": ["pos_hr"],
    "author": "danal",
    "category": "Category",
    "license": "LGPL-3",
    "data": [
        "views/pos_order_view.xml",
    ],
    "assets": {"point_of_sale._assets_pos": ["pos_order_salesperson/static/src/**/*"]},
}
