{
    "name": "Extend Warranty",
    "version": "1.0",
    "depends": ["base", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_warranty_wizard_views.xml",
        "views/product_template_views.xml",
        "views/warranty_config_views.xml",
        "views/sale_order_views.xml",
        "views/warranty_menu_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
