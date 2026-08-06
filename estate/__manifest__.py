{
    "name": "real estate",
    "author": "Lokesh",
    "version": "1.0.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_actions.xml",  # the order should be like this, first we need to define the action and then we need to define the menu and then the views if the order is not maintained then error will be thrown.
        "views/estate_property_views.xml",
        "views/estate_property_menu.xml",
    ],
}
