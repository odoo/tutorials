{
    "name": "Budget Management",
    "category": "Accounting/Budgeting",
    "depends": ["base", "account"],
    "description": """
            This module is for managing Budgets.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/budget_views.xml",
        "views/budget_lines_views.xml",
        "wizard/bulk_budget_views.xml",
        "views/budget_menus.xml",
    ],
    "demo": [],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
