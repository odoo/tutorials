{
    "name": "product_warranty",
    "summary": "Add product warranty",
    "description": "Add product warranty (ddba)",
    "author": "Odoo",
    "category": "Tutorials/product_warranty",
    "version": "1.5",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        
        "wizard/product_warranty_wizard_views.xml",

        "views/product_views.xml",
        "views/product_warranty_views.xml",
        "views/sale_order_form_view.xml",
        "views/sale_menus.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
