{
    "name": "Budget Management",
    "summary": "Module for managing budgets",
    "description": "Module for managing budgets",
    "category": "Account/ Budget Management",
    "version": "1.0",
    "application": True,
    "installable": True,
    "depends": ["base", "analytic"],
    "data": [
        "security/ir.model.access.csv",
        "views/analytic_line_views.xml",
        "views/budget_budget_line_views.xml",
        "views/budget_budget_views.xml",
        "views/budget_budget_menu_views.xml",
        "wizard/budget_wizard_views.xml",
    ],
    "license": "AGPL-3",
}
