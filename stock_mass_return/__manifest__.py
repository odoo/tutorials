# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stock Mass Return",
    "version": "1.0",
    "summary": "Handle mass return functionality for done transfers",
    "depends": [
        "stock",
        "stock_accountant",
        "sale_management",
        "purchase"
    ],
    "data": ["wizard/stock_picking_return_views.xml"],
    "license": "LGPL-3",
}
