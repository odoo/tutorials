# -*- coding: utf-8 -*-

{
    "name": "Sell Product Kit",
    "summary": "A module to create an option to sell a product as kit",
    "depends": ["product", "sale", 'sale_management'],
    "data" : [
        "security/ir.model.access.csv",
        "views/product_kit_wizard_view.xml",
        "views/sales_order_line_form_view.xml",
        "views/product_template_form_view.xml",
        "reports/sale_order_document_report.xml",
        "reports/sale_portal_templates_report.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
