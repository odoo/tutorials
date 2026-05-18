{
    "name": "Redesign Catalog View",
    "version": "1.0",
    "category": "Sales",
    "author": "habar",
    "depends": ["sale", "sale_stock"],
    "data": [
        "views/product_view_kanban_catalog_inherit.xml"
    ],
    "application": False,
    "license": "LGPL-3",
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "sale_catalog_redesigner/static/src/components/product_image_dialog.js",
            "sale_catalog_redesigner/static/src/components/product_image_dialog.xml",
            "sale_catalog_redesigner/static/src/components/product_image.js",
            "sale_catalog_redesigner/static/src/components/product_image.xml",
            "sale_catalog_redesigner/static/src/scss/catalog_zoom.scss"
        ],
    },
}
