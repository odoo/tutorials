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
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/product_views.xml",
        "wizard/add_warranty_wizard.xml",
        "wizard/list_warranty_wizard.xml",
        "views/product_warranty_views.xml",
        "views/sale_menus.xml",
    ],
    "license": "AGPL-3",
}
