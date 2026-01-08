{
    "name": "Product Warranty",
    "depends": [
        "sale_management",
        "website_sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/order_wizard_view.xml",
        "views/product_template_view.xml",
        "views/warranty_configration.xml",
        "views/warranty_configration_menu.xml",
        "views/sale_order_views.xml",
    ],
    "demo": [
        "demo/product_warranty_demo.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
