{
    "name": "product_warranty",
    "author": "Bhavya Nanavati",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template.xml",
        "wizard/warranty_configuration_wizard_views.xml",
        "views/warranty_configuration_views.xml",
        "views/warranty_configuration_menuitem.xml",
        "views/warranty_configuration_wizard_button.xml",
    ],
    "demo": [
        "demo/product_warranty_demo.xml"
    ],
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
