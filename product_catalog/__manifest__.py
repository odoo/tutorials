{
    "name": "Product Catalog Redesign",
    "version": "1.0",
    "category": "Sales",
    "depends": ["product", "sale_management"],
    "data": ["views/product_catalog_view.xml"],
    "application": True,
    "assets": {
        "web.assets_backend": [
            "product_catalog/static/src/scss/product_catalog.scss",
            "product_catalog/static/src/js/product_catalog.js",
            "product_catalog/static/src/js/image_preview/image_preview.xml",
            "product_catalog/static/src/js/screen_container/screen_container.xml",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
}
