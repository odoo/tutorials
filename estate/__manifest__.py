{
    "name": "Real Estate",
    "author": "Lokesh",
    "version": "1.0.0",
    "license": "LGPL-3",
    "depends": ["base"],
    'category': 'Real Estate/Brokerage',
    "application": True,
    "installable": True,
    'demo': [
        'demo/estate_property_data.xml',
    ],
    "data": [
        'security/estate_security.xml',
        "security/ir.model.access.csv",
        # the order should be like this, first we need to define the views and then we need to define the action and then the menu if the order is not maintained then error will be thrown.
        "views/estate_property_views.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/estate.css",
        ],
    },
}
