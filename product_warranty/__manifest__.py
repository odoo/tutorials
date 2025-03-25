{
    "name": "Product Warranty",
    "version": "1.0",
    "depends": ["sale_management", "stock", "website_sale"],
    "author": "Odoo",
    "website": "www.odoo.com/",
    "license": "LGPL-3",
    "description": "Product Warranty",
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_warranty_views.xml",
        "wizard/product_warranty_wizard_views.xml",
        "views/sale_order_line_views.xml",
        "views/product_warranty_menus.xml",
    ],
    "application": True,
    "installable": True,
}
