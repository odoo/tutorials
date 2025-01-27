{
    "name": "product_type",
    "summary": "Add new product_type",
    "description": "Add Add new product_type (yame)",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Tutorials/product_warranty",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "stock", "sale_management"],
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "report/sale_order_report.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml",
        "wizard/list_product_wizard.xml",
        "wizard/add_product_wizard.xml",
    ],
    "license": "AGPL-3",
}
