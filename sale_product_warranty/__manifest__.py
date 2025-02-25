{
    "name": "Product Warranty",
    "description": "Adds functionality to manage product warranties in sales orders and linking warranties to products",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/warranty_configuration_views.xml",
        "views/warranty_configuration_menus.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "wizard/sale_order_add_warranty_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
