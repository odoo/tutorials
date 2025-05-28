{
    "name": "Product Warranty",
    "version": "1.0",
    "description": "Product Warranty",
    "author": "Abhishek Khant (abhk)",
    "depends": ["sale", "product"],
    "data": [
        "security/ir.model.access.csv",
        "data/product_warranty_data.xml",
        "views/product_template_views.xml",
        "views/product_warranty_views.xml",
        "wizard/product_warranty_wizard_views.xml",
        "views/sale_order_line_views.xml",
        "views/product_warranty_menus.xml",
    ],
    "auto_install": True,
    "license": "LGPL-3",
}
