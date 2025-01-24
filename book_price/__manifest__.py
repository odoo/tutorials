# -*- coding: utf-8 -*-
{
    "name": "book_price",
    "summary": "Add Pricelist Price (yame)",
    "description": "Add Pricelist Price (yame)",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/book_price",
    "version": "0.1",
    "depends": ["base", "web", "sale", "sale_management", "account"],
    "installable": True,
    "data": [
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
    ],
    "license": "AGPL-3",
}
