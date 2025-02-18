{
    "name": "estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "Odoo S.A.",
    "category": "Category",
    "description": """
        This is a module to manage real estate properties
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "application": True,
    "license": "LGPL-3",
}
