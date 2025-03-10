{
    "name": "coatations_claims",
    "depends": ["sale_management", "website", "approvals"],
    "data": [
        "security/ir.model.access.csv",
        "views/coatation_view.xml",
        "views/coatation_claims_menus.xml",
        "wizard/coation_price_wizard.xml",
        "views/sale_order_line_form_inherit.xml",
        "report/coatation_claims_template.xml",
        "report/coatation_claims.xml"
    ],
    "application": True,
    "license": "LGPL-3",
}
