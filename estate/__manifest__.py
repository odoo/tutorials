# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Make your real estate management easy!",
    "category": "Tutorials/RealEstate",
    "depends": ["base", "mail", "website"],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/website_menu_data.xml",
        "reports/estate_property_templates.xml",
        "reports/estate_property_reports.xml",
        "wizard/res_config_settings.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_menu_views.xml",
        "views/estate_property_templates.xml",
        "views/portal_templates.xml",
    ],
    "demo": [
        "data/estate_property_type_demo.xml",
        "data/estate_property_demo.xml",
        "data/estate_property_offer_demo.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
