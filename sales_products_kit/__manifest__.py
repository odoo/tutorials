{
    "name": "Sales - Product_Kit",
    "version": "1.0",
    "description": """
        This custom module adds a function to Odoo to sell products as a Kit, but not using a BOM or the Manufacturing Module.
        """,
    "category": "Sales/Sales",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sub_product_wizard.xml",
        "views/product_view.xml",
        "views/sale_order_view.xml",
        "report/sale_order_report.xml",
        "views/sale_portal_templates.xml",
        "report/invoice_report.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
