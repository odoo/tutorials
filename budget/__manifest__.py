{
    "name": "Budget",
    "version": "1.0",
    "depends": ["account"],
    "category": "Accounting/Budget",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/multiple_budgets_views.xml",
        "views/budget_budget_views.xml",
        "views/budget_line_views.xml",
        "views/budget_menus.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
