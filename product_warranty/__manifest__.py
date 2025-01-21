# -*- coding: utf-8 -*-
{
    "name": "product_warranty",
    "summary": "Add product warranty",
    "description": "Add product warranty (yame)",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/product_warranty",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "stock", "sale_management"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
    ],
    "license": "AGPL-3",
}
