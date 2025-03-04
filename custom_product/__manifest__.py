{
    "name": "Costom Product",
    "version": "1.0",
    "depends": ["sale"],
    "author": "Darshan Patel",
    "category": "Sales",
    "license": "LGPL-3",
    "summary": "Sell products as a kit without BoM",
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "wizard/sale_kit_wizard_view.xml",
        "views/sale_order_views.xml",
        # "reports/sale_order_report.xml"
    ],
    "installable": True,
    "application": True,
}
