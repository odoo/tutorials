{
    "name": "purchase discount",
    "version": "1.0.0",
    "depends": ["base", "purchase"],
    "author": "Mehul Kotak",
    "category": "Task-1",
    "description": "This perfrom global discount in purchase",
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "wizard/purchase_order_discount.xml",
    ],
}
