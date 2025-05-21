{
    "name": "estate",
    "description": """
        This module is used to manage the Real estate and properties.
    """,
    "author": "ayush",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base"],
    "license": "LGPL-3",
    "category": "Real Estate/Brokerage",
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
        "data/estate_property_type_demo.xml",
    ],
    "demo": [
        "data/estate_property_demo.xml",
        "data/estate_property_offer_demo.xml",
    ],
}
