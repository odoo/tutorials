{
    "name": "Estate",
    "depends": ["base", "mail"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/maintenance_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "data/booking_sequence.xml",
        "data/estate_property_type.xml",
        "data/estate_property_tag.xml",
        "data/estate_property_demo.xml",
        "views/estate_property_booking_views.xml",
        "views/estate_property_payment_views.xml",
        "views/estate_menus.xml",

    ],
    "author": "dheer",
    "license": "LGPL-3",
}
