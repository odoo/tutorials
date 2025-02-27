# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sale Warranty",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Add warranty to products!",
    "category": "Tutorials/Sale Warranty",
    "depends": ["product", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/product_warranty_views.xml",
        "views/sale_menus.xml",
        "views/sale_order_views.xml",
        "wizard/sale_order_warranty_views.xml"
    ],
    "installable": True,
    "license": "LGPL-3"
}
