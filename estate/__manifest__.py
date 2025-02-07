{
    "name": "estate",
    "depends": ["base"],
    "sequence": 1,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/property_type_views.xml",
        "views/property_tags_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
