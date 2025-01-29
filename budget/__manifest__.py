{
    "name": "Budget Management | KSAR",
    "description": "Creating and managing the budgets",
    'icon': '/budget/static/description/icon.png',
    "installable": True,
    "application": True,
    "depends": ["base", "account", "web_gantt", "portal"],
    "data": [
        "security/ir.model.access.csv",
        "views/budget_line_views.xml",
        "views/budget_views.xml",
        "views/budget_menus.xml",
        "views/account_analytics_line_view.xml",
        "wizard/budget_generate_wizard_view.xml",
    ],
    "license": "LGPL-3",
}
