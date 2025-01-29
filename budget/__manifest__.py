# -*- coding: utf-8 -*-
{
    "name": "budget",
    "summary": "budget (yame)",
    "description": "budget (yame)",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/budget",
    "version": "0.1",
    "depends": ["base", "web", "account"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_line.xml",
        "wizard/budget_wizard_view.xml",
        "views/budget_budget_views.xml",
        "views/budget_line_views.xml",
        "views/budget_menu.xml",
    ],
    "license": "AGPL-3",
}
