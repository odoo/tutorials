{
    "name": "Warranty",
    "description": "Adding Warranty",
    "version": "0.1",
    "depends": ["base", "account", "sale_management", "stock"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_warranty_wizard.xml",
        "views/warranty_views.xml",
        "views/product_template_views.xml",
        "views/sale_order.xml",
        "views/warranty_menuitem.xml",
    ],
    "license": "LGPL-3",
}
