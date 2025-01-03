{
    "name": "Budget",
    "version": "1.0",
    "summary": "Budget Management",
    "depends": ["account"],
    "category": "Accounting/Budget",
    "data": [
        "security/ir.model.access.csv",
        "wizard/multiple_budgets_wizard_views.xml",
        "views/account_analytic_line_main.xml",
        "views/budget_line_views.xml",
        "views/budget_budget_views.xml",
        "views/budget_management_menus.xml",
    ],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
}
