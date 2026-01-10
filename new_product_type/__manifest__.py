{
    "name": "New Product Type",
    "description": """
        "
    """,
    "version": "0.1",
    "depends": ['sale_management'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template.xml",
        "views/sale_order.xml",
        "views/sale_order_report.xml",
        "wizard/sale_order_wizard.xml"
    ],
    "assets": {},
    "license": "AGPL-3",
    "installable": True,
    "auto-install": True,
}
