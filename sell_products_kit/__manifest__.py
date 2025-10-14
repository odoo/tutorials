{
    "name": "sell_products_kit",
    "version": "1.0",
    "author": "assh-odoo",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "report/ir_actions_report_template.xml",
        "views/sale_portal_template.xml",
        "wizard/sub_product_wizard_view.xml",
        "views/product_template_views.xml",
        "views/sale_oders_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
