{
    "name": "Warranty",
    "version": "1.0",
    "description": "Warranty Management",
    "depends": ['sale_management'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/warranty_views.xml",
        "wizard/warranty_wizard_views.xml",
        "views/sale_order_views.xml",
    ],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
}
