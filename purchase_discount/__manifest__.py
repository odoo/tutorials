{
    "name": "purchase discount",
    "version": "1.0.0",
    "depends": ["base", "purchase"],
    "author": "Mehul Kotak",
    "category": "Task-1",
    "description": "This perfrom global discount in purchase",
    "license": "LGPL-3",
    "auto_install": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/purchase_order_discount.xml",
        "views/purchase_order_view.xml",
    ],
}
