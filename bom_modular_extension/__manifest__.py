{
    "name": "BOM Modular Extension",
    "description": "Add modular types and multiplies MO line quantity by SO values",
    "version": "1.0",
    "depends": ["sale_management", "mrp", "product"],
    "category": "Manufacturing",
    "data": [
        "security/ir.model.access.csv",
        "views/product_template.xml",
        "views/mrp_bom_line.xml",
        "wizard/sale_order_line_wizard.xml",
        "views/sale_order_button.xml",
        "views/mrp_production.xml",
    ],
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
