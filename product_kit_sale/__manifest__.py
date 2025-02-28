# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Product Kit Sale",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Allows selling products as kits.",
    "category": "Tutorials/Product Kit Sale",
    "depends": ["sale_management", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/product_template_views.xml",
        "wizard/sale_order_kit.xml"
    ],
    "installable": True,
    "license": "LGPL-3"
}
