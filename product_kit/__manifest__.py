{
    "name": "product_kit",
    "version": "1.0",
    "description": "product kit",
    "summary": "will allow you to add extra product with main product as a kit.",
    "author": "Odoo",
    "website": "www.odoo.com",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/product_kit_wizard_views.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml",
    ],
    "application": True,
    "installable": True,
}
