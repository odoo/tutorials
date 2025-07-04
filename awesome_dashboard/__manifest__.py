# -*- coding: utf-8 -*-
{
    "name": "Awesome Dashboard",
    "summary": """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
    "description": """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com/",
    "category": "Tutorials/AwesomeDashboard",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base", "web", "mail", "crm"],
    "data": [
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "awesome_dashboard/static/src/dashboard/dashboard_action.js",
            "awesome_dashboard/static/src/dashboard/dashboard_action.xml",
            "awesome_dashboard/static/src/dashboard/services/statistics.js",
        ],
        "awesome_dashboard.dashboard": [
            "awesome_dashboard/static/src/dashboard/services/statistics.js",
            "awesome_dashboard/static/src/dashboard/components/dashboard_settings_dialog.js",
            "awesome_dashboard/static/src/dashboard/components/dashboard_settings_dialog.xml",
            "awesome_dashboard/static/src/dashboard/dashboard.js",
            "awesome_dashboard/static/src/dashboard/dashboard_items.js",
            "awesome_dashboard/static/src/dashboard/components/*.js",
            "awesome_dashboard/static/src/dashboard/components/*.xml",
            "awesome_dashboard/static/src/dashboard/*.xml",
            "awesome_dashboard/static/src/dashboard/*.scss",
        ],
    },
    "license": "AGPL-3",
}
