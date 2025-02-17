{
    "name": "Real Estate",
    "version": "1.0",
    "summary": "Manage real estate properties and transactions",
    "category": "Real Estate/Brokerage",
    "description": """
        This module allows users to manage real estate listings, 
        offers, and transactions efficiently.
    """,
    "author": "Dev Patel",
    "license": "LGPL-3",
    "depends": ["base","mail"],
    "data": [
        "security/security.xml",
        "security/custom_group_user.xml",
        "data/estate_property_type_demo_data.xml",
        "data/estate_property_demo_data.xml",
        "data/estate_property_offer_demo_data.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_users_views.xml",
        "views/estate_menus.xml",
        "security/ir.model.access.csv",
    ],
    "application": True,
    "auto_install": False,
}
