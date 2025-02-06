{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "odoo",
    "license": "LGPL-3",
    "description": """
This is Real Estate application which makes easy to sold property
    """,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_menus.xml",
    ],
}
