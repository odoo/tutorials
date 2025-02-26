{
    "name": "Book price in sales and invoices",
    "category": "Sales",
    "description": """add computed field 'Book Price' to Sale Order Lines and Account Move Lines.""",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_line_view.xml",
        "views/account_move_line_view.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
