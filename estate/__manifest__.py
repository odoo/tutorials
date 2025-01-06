{
    "name": "Estate",
    "summary": """
        Starting module for "Master the Odoo web framework, chapter 1: Build a Clicker game"
    """,
    "description": """
        Starting module for "Master the Odoo web framework, chapter 1: Build a Clicker game"
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/Estate",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/res_users_views.xml",
        "views/estate_menu_views.xml",
    ],
    "license": "AGPL-3",
}
