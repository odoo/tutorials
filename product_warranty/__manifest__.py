{
    "name": "Product Warranty",
    "version": "1.0",
    "category": "Sales/Warranty",
    "summary": "Add warranty information to products and display it on sale order lines.",
    "description": """
This module provides functionality to manage product warranties.
Users can define warranties for products and see warranty details in sale order lines.
""",
    "license": "AGPL-3",
    "depends": ["base", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_warranty_config_views.xml",
        "views/product_warranty_config_menu.xml",
        "views/sale_order_views.xml",
        "wizard/product_warranty_wizard_view.xml",
    ],
    "auto_install": True,
}
