{
    "name": "Distribute Price",
    "description": "Distribute Cost Over other sale order line",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "wizard/sale_order_distribute_views.xml",
        "report/sale_order_report.xml",
    ],
    "installable": True,
    "license": "LGPL-3"
}
