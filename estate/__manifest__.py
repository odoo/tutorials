{
    "name": "Real Estate",
    "category": "Tutorials",
    "summary": "Real Estate App",
    "installable": True,
    "application": True,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "auto_install": False,
    "author": "Rohit Agarkar",
    "license": "LGPL-3",
}
