{
    "name": "Real Estate",
    "version": "1.0",
    "summary": "Manage real estate properties and transactions",
    "category": "Real Estate",
    "description": """
        This module allows users to manage real estate listings, 
        offers, and transactions efficiently.
    """,
    "author": "Dev Patel",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/custom_group_user.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_view.xml",
        "views/estate_menus.xml",
    ],
    "application": True,
    "auto_install": False,
}
