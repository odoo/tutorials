# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Dream Homes",
    "version": "1.0",
    "depends": ["base", "mail"],
    "category": "Real Estate/Brokerage",
    "data": [
        "security/estate_property_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_menus.xml",
        "views/res_users_views.xml",
        "data/estate.property.types.csv",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
