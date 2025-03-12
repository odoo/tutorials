{
    "name": "Modular Types",
    "version": "1.0",
    "summary": "Dynamically adjust manufacturing order quantities from sales order.",
    "description": "Dynamically multiply manufacturing order component quantities based on sales order line factors.",
    "category": "Sales",
    "author": "Darshan Patel",
    "license": "LGPL-3",
    "depends": ["sale_management", "mrp", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/modular_type_wizard.xml",
        "views/product_template_views.xml",
        "views/mrp_bom_views.xml",
        "views/mrp_production_view.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
