{
    "name": "Modular MRP",
    "version": "1.0",
    "description": """Add modular types on products for MRP quantity multiplication.""",
    "author": "Soham",
    "depends": [
        "product",
        "mrp",
        "sale_management",
        "sale_mrp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/mrp_bom_views.xml",
        "views/sale_line_modular_value_wizard_views.xml",
        "views/sale_order_views.xml",
    ],
    "license": "LGPL-3",
}
