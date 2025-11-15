{
    "name": "Custom Product Kit",
    "category": "Sales",
    "description": """
        This module allows users to mark a product as a kit and assign multiple sub-products.
    """,
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "report/sale_order_report.xml",
        "report/report_invoice.xml",
        "report/sale_portal_templates.xml",
        "views/product_form_view.xml",
        "views/sale_order_form_view.xml",
        "wizard/product_kit_wizard_view.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
