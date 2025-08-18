{
    "name": "WSCS_product_extension_app",
    "author": "Bhavya Nanavati",
    "depends": ["stock", "mrp", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_views.xml",
        "views/product_status_views.xml",
        "views/product_template_inherit.xml",
        "views/product_packaging_views.xml",
        "views/product_palletspec_views.xml",
        "views/menuitems.xml",
        "data/product_status_data.xml",
    ],
    "auto_install": True,
    "license": "LGPL-3",
}
