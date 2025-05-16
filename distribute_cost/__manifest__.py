{
    "name": "Distribute Cost Over other sales line",
    "depends": ["sale_management"],
    "license": "LGPL-3",
    "auto_install": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "wizard/distribute_cost_wizard_views.xml",
        "report/sale_order_report.xml"
    ],
}
