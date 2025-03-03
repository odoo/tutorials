{
    "name": "Sales kit",
    "description": """
    sales kit integration
    """,
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "report/sale_order_report.xml",
        "report/invoice_report.xml",
        "report/sale_portal_customer_view.xml",
        "views/product_template_views.xml",
        "views/sale_order_line.xml",
        "wizard/sub_product_wizard_view.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
