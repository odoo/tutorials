{
    "name": "estate",
    "sequence": 1,
    "description": "",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_user_views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
