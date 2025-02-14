{
    "name": "estate",
    "version": "1.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/res_user.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,  # this makes the applications available even in app filter is on
    "auto-install": False,
}
