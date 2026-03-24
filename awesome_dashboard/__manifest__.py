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
    "category": "Tutorials",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base", "web", "mail", "crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "awesome_dashboard/static/src/dashboard_action.js",
            "awesome_dashboard/static/src/about.js",
        ],
        "awesome_dashboard.dashboard_assets": [
            "awesome_dashboard/static/src/dashboard/**/*",
            "awesome_dashboard/static/src/services/stats_service.js",
            "awesome_dashboard/static/src/services/dashboard_item_service.js",
        ],
    },
    "license": "AGPL-3",
}
