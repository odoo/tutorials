{
    "name": "Sale Warranty",
    "summary": "Adds configurable warranties for products in sales.",
    "description": """
        Enhance Odoo by adding a warranty feature that allows users to configure and select extended
        warranties for products.The functionality includes a new warranty configuration model,
        a button in sales orders to add warranties, and automatic price computation based on
        predefined percentages.Warranty details appear as separate line items in quotations and invoices
    """,
    "author": "Khushi",
    "category": "Sales",
    "version": "1.0",
    "depends": ["sale_management", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/warranty_configuration_views.xml",
        "views/warranty_configuration_menus.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "wizard/sale_order_add_warranty_views.xml",
    ],
    "installable": True,
    "auto-installable":True,
    "application": False,
    "license": "LGPL-3"
}
