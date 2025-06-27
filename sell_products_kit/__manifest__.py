{
    "name": "Sell products kit",
    "version": "1.0",
    "depends": ["sale_management"],
    "license": "LGPL-3",
    "data": [
        "views/product_template_view.xml",
        "views/sales_order_view.xml",
        "security/ir.model.access.csv",
        "wizard/sub_product_wizard_view.xml",
        "wizard/sub_product_wizard_line_view.xml",
    ],
    "installable": True,
    "application": True,
}
