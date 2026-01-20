{
    "name": "Redesign Catalog View",
    "version": "1.0",
    "depends": ["purchase"],
    "data": ["views/redesign_catalog_view.xml"],
    "appication": True,
    "sequence": 1,
    "license": "LGPL-3",
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "redesign_catalog_view/static/src/**/*",
        ],
    },
}
