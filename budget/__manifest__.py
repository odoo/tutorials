{
    "name": "Budget",
    "version": "1.0",
    "category": "Accounting",
    "summary": "Manage budgets for companies",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/budget_wizard_views.xml",
        "views/budget_lines_views.xml",
        "views/budget_views.xml",
        "views/budget_menus.xml",
    ],
    'images': ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
