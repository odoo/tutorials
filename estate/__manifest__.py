{
    "name": "Real Estate",
    "depends": ["base"],
    "application": True,
    "installable": True,
    "author": "Aditya Maurya",
    "license": "LGPL-3",
    "category": "Real Estate",
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menu.xml",
    ],
    "demo": [
        "data/estate_property_demo.xml",
    ],
}
