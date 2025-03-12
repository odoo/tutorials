{
    "name": "custom_product",
    "author": "dijo",
    "version": "1.2",
    "summary": "This is product module developed by deep i. joshi",
    "category": "Sales/Sales",
    "license": "LGPL-3",  # removed application : True
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "report/sale_order_report.xml",
        "views/sale_portal_template.xml",
        "views/sale_order_views.xml",
        "wizard/kit_wizard.xml",
    ],
}
