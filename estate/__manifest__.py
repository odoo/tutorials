{
    "name": "Real Estate",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    "summary": "Manage real estate properties and offers",
    "description": "This is my first estate module.",
    "author": "Gautam",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_menu.xml",
    ],
    "demo": [
        "demo/demo_estate_property.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": True,
}
