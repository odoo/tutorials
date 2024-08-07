{
    "name": "Real Estate",
    "version": "1.0",
    "license": "LGPL-3",
    "category": "Real Estate",
    "summary": "Manage properties",
    "depends": ["base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "views/real_estate_property.xml",
        "views/estate_property_tree_views.xml",
        "views/property_type_views.xml",
        "views/property_tag.xml",
        "views/real_estate_menu.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
