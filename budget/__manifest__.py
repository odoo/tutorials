{
    "name": "Budget Management",
    "version": "1.0",
    "license": "LGPL-3",
    "depends": [
        "account",
        "analytic",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/multiple_budget_wizard_views.xml",
        "views/account_analytic_line_views.xml",
        "views/budget_line_views.xml",
        "views/budget_budget_views.xml",
        "views/budget_menu.xml"
    ],
    "installable": True,
    "application": True
}