# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate",
    "author": "nmak",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "report/estate_property_report_views.xml",
        "report/estate_property_reports.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
