{
    "name": "Distribute Cost",
    "version": "1.0",
    "summary": "Adds cost distribution functionality to sale order lines",
    "author": "Harsh Shah (hash)",
    "category": "Sales",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_line_view.xml",
        "views/sale_order_line_share_wizard_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
