{
    "name": "Real Estate Invoicing",
    "version": "0.1",
    "category": "Administration",
    "sequence": 100,
    "license": "LGPL-3",
    "author": "Odoo S.A.",
    "summary": "Provides invoicing for the estate app",
    "description": "",
    "website": "https://www.odoo.com/page/estate",
    "depends": ["estate", "account"],
    "data": [
        "views/estate_property_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
