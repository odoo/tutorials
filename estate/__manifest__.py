
{
    "name": "real state",
    "description": "This is my first module estate",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_view.xml",
        "views/estate_menu.xml",
    ],
    "demo": [
        "demo/demo_estate_property.xml",
    ],
    "application": True,
    "installable": True,
    "author": "Gautam",
    "license": "LGPL-3",
    "auto_install": True,
}
