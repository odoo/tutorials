{
    "name": "Real_estate",
    "version": "1.8",
    "summary": "Track leads and close opportunities",
    "depends": [
        "base_setup",
    ],
    "data": [
        "security/ir.model.access.csv",

        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
