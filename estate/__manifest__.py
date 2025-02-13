{
    "name": "estate",
    "version": "1.0",
    "summary": "Manage real estate properties, offers, and sales",
    "sequence": 15,
    "description": """ 
        This module helps manage real estate properties, track offers, and handle sales.
    """,
    "category": "Real Estate/Brokerage",
    "author": "Darshan Patel",
    "website": "",
    "depends": ["base","mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_tag.xml",
        "views/res_user.xml",
        "views/estate_property_offer.xml",
        "views/estate_property_type.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "data/estate_property_type_data.xml",
        "data/mail_message_subtype_data.xml"
    ],
    "demo": [
        "demo/estate_demo_properties.xml",
        "demo/estate_demo_offers.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
