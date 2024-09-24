{
    "name": "Product Warranty",
    "version": "1.0",
    "license": "LGPL-3",
    "depends": ["base","stock","sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_warranty_button_action.xml",
        "views/inherit_product_template.xml",
        "views/add_warranty_button.xml",
        "views/waranty_configuration_views.xml",
        "views/warranty_configuration.xml",
    ],
    "installable": True,
    "application": True,
}
