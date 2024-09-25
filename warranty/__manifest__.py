{
    "name": "warranty",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "stock", "sale_management"],
    "description": "Adding warranty",
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/warranty_view.xml",
        "views/warranty_menus.xml",
        "views/product_view.xml",
        "wizard/add_warranty_view.xml",
        "views/sale_order_view.xml",
    ],
}
