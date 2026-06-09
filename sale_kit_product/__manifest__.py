{
    "name": "Sale Kit Product",
    "application": False,
    "installable": True,
    "author": "sngoh",
    "depends": ["base", "product", "sale"],
    "auto_install": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_kit_product_wizard_view.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
}
