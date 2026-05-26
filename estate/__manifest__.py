{
    "name": "estate",
    "version": "1.0",
    "summary": "Estate management",
    "description": "Estate management",
    "author": "Odoo S.A.",
    "website": "https://www.odoo.com/",
    "license": "LGPL-3",
    "category": "Uncategorized",  # Module category in Odoo apps
    "depends": ["base"],          # Required dependency modules
    "installable": True,          # Allows module installation
    "application": True,          # Shows as main application
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
}

