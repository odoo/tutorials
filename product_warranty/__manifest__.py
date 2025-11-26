{
    "name": "product_warranty",
    "summary": "Add product warranty",
    "description": "Add product warranty",
    "author": "Odoo",
    "category": "Tutorials/product_warranty",
    "version": "1.0",
    "depends": ["base", "sale_management"], 
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_warranty_views.xml",
        "views/sale_order_views.xml",
        "views/product_warranty_menu.xml",
        "wizard/add_warranty_wizard_views.xml",
    ],
    "demo": [
        "demo/data.xml",
    ],
    "license": "AGPL-3",
}
