{
    "name": "purchase_dicount",
    "description": "Add discount button with its wizard",
    "author": "odoo-pupat",
    "website": "https://www.odoo.com/",
    "category": "Purchase-custom",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_views.xml",
        "wizard/purchase_order_discount_views.xml",
    ],
    "assets": {},
    "license": "LGPL-3",
}
