{
    "name": "New Product Type",
    "description": "New Product Type in Odoo",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_form_view.xml",
        "views/sale_order_view.xml",
        "views/sale_order_portal_content.xml",
        "report/report_invoice_document.xml",
        "report/report_saleorder_document.xml",
        "wizard/subproducts_wizard_view.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
