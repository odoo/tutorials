{
    "name": "Book Price Pricelist",
    "version": "1.0",
    "description": "book price pricelist",
    "summary": "book price pricelist",
    "author": "Odoo",
    "website": "www.odoo.com",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_line_views.xml",
        "views/account_move_line_views.xml",
    ],
    "application": True,
    "installable": True,
}
