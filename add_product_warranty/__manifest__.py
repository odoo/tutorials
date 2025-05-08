{
    "name": "Add Warranty Product",
    "description": """
 The Module helps to add warranty to our product
    """,
    "version": "1.0",
    "depends": ["product", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_warranty.xml",
        "views/warranty_menus.xml",
        "views/product_template.xml",
        "views/sale_order_button.xml",
        "wizard/add_warranty_wizard.xml",
    ],
    "auto-install": True,
    "application": False,
    "license": "LGPL-3",
}
