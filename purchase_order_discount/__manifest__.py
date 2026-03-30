{
    "name": "Purchase Order Discount",
    "version": "1.0",
    "category": "Purchase",
    "description": "Purchase order global discount wizard.",
    "author": "juson-odoo",
    "depends": ["base", "purchase"],
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_views.xml",
        "wizard/purchase_order_discount.xml",
    ],
}
