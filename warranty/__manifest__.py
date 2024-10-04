{
    "name": "warranty",
    "depends": ["base", "sale_subscription"],
    "Description": "warranty_Module",
    "license": "LGPL-3",
    "summary": "warranty module for different purpose",
    "author": "koye_odoo",
    "version": "0.0.1",
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_warranty_view.xml",
        "views/warranty_config_view.xml",
        "views/sale_order_view.xml",
        "views/product_template_view.xml",
    ],
}
