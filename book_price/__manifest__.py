{
    "name": "Sale Book Price",
    "version": "1.0",
    "category": "Sales/Book Price",
    "summary": "Added book price",
    "description": """
        Added book price in sales order line and account move line
        so that customer can see difference between Pricelist price and other modified price.""",
    "depends": ["sale"],
    "data": [
        "views/sale_order_line_views.xml", 
        "views/account_move_line_views.xml"
    ],
    "installable": True,
    "license": "LGPL-3",
}
