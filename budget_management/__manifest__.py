{
    "name": "Budget Management",
    "category": "Budget",
    "version": "1.0",
    "depends": ["base", "account", "accountant"],
    "author": "djip-odoo",
    "description": """
        Part of technical training
        Creating Budget Management module as review task
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/budget_line_views.xml",
        "views/actions_menu_and_button.xml",
        "views/menu_views.xml",
        "views/budget_views.xml",
        "wizards/wizard_add_budgets_view.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
