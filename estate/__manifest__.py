{
    "name": "real estate",
    "author": "Lokesh",
    "version": "1.0.0",
    "license": "LGPL-3",
    # "depends": ["base"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",  # the order should be like this, first we need to define the views and then we need to define the action and then the menu if the order is not maintained then error will be thrown.
        "views/estate_property_type_view.xml",
        "views/estate_property_menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/estate.css",
        ],
    },
}
