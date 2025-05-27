{
    "name": "Redesign Catalog",
    "version": "1.0",
    "author": "rpka",
    "depends": ["sale_management"],
    "data": [
        "views/product_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_catalog_redesign/static/src/**/*.js",
            "product_catalog_redesign/static/src/**/*.scss",
            "product_catalog_redesign/static/src/**/*.xml",
        ]
    },
    "installable": True,
    "license": "LGPL-3",
}
