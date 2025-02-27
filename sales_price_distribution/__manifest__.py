{
    "name": "Sales Price Distribution",
    "version": "1.0",
    "summary": "Distribute Cost Over other sales line",
    "description": """
        Distribute Cost Over other sales line
    """,
    "author": "Odoo",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "wizards/price_distribution_wizard.xml",
        "views/sale_order_line_views.xml",
        "security/ir.model.access.csv",
        "report/ir_actions_report_templates.xml",
    ],
}
