{
    "name": "Real Estate",
    "description": """
Assets management
=================
Manage assets owned by a company or a person.
Keeps track of depreciations, and creates corresponding journal entries.

    """,
    "version": "1.8",
    "category": "All",
    "sequence": 15,
    "summary": "Manage your residential opps",
    "depends": [
        "base_setup",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": True,
    "assets": {},
    "license": "LGPL-3",
}
