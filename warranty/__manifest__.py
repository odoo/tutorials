{
    "name": "warranty",
    "depends": ["base", "stock", "sale_management"],
    "Description": "warranty_Module",
    "license": "LGPL-3",
    "summary": "warranty module for different purpose",
    "author": "koye_odoo",
    "version": "0.0.1",
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/warranty_configuration_views.xml",
        "views/warranty_configuration_menus.xml",
        "wizard/wizard_view.xml",
        "views/sale_order_line_view.xml",
    ],
}
