{
    "name": "Real Estate",
    "version": "19.0.0",
    "category": "Tutorials",
    "depends": ["base"],
    "author": "hemeh",
    "application": True,
    "summary": "Manage real estate properties",
    "description": """
    Manage real estate properties.
    """,
    "website": "https://odoo.com",
    "license": "LGPL-3",
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
}
