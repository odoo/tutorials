{
    "name": "Warranty",
    "version": "1.0",
    "description": "Adding warranty",
    "author": "Akya",
    "depends": ["base", "sale_subscription"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_warranty_view.xml",
        "views/warranty_config_view.xml",
        "views/sale_order_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
