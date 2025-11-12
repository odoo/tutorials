{
    "name": "Budget",
    "version": "1.0",
    "depends": ["base","account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/budget_wizard_views.xml",
        "views/budget_views.xml",
        "views/budget_line_views.xml",
        "views/budget_menu_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}