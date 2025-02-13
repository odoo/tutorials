{
    "name": "estate app",
    "description": """
        A real estate application for selling and renting properties
    """,
    "author": "Odoo",
    "category": "Real Estate/Brokerage",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/estate_users_views.xml",
    ],
    "license": "AGPL-3",
}
