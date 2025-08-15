{
    "name": "Product Warranty",
    "depends": ["stock", "sale_management"],
    "license": "LGPL-3",
    "auto_install": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/product_warranty_views.xml",
        "views/warranty_menus.xml",
        "wizard/add_warranty_wizard.xml",
    ],
}
