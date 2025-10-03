{
    "name": "Purchase Order Print",
    "version": "1.0",
    "summary": "Custom module to print purchase orders with additional fields.",
    "author": "Ayush Patel",
    "depends": ["purchase", "base", "hr"],
    "license": "LGPL-3",
    "data": [
        "reports/custom_purchase_report_template.xml",
        "views/hr_employee_model_fields.xml",
        "views/hr_employee_views.xml",
        "views/product_model_fields.xml",
        "views/product_template_views.xml",
        "views/purchase_order_model_fields.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
    "application": True,
}