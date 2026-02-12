{
    "name": "Modular Types",
    "version": "1.0",
    "category": "Manufacturing",
    "author": "Abhi Bhingradiya(abbhi)",
    "description": """
        This module allows adding modular types to products and BoM lines.
        In Sales Orders, users can set values for these modular types, which
        will then be used to multiply the quantities in the resulting Manufacturing Orders.
    """,
    "depends": ["sale_management", "mrp", "sale_mrp"],
    "data": [
        "security/ir.model.access.csv",
        "views/modular_type_views.xml",
        "views/product_views.xml",
        "views/mrp_bom_views.xml",
        "views/sale_order_views.xml",
    ],
    "license": "LGPL-3",
}
