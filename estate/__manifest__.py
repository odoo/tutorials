# -*- coding: utf-8 -*-
{
    "name": "estate",
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Real Estate/Brokerage",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "website"],
    "application": True,
    "installable": True,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/property_website_list_template.xml",
        "wizard/wizard_property_offers_view.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/inherited_user_view.xml",
        "views/estate_property_menu.xml",
        "data/estate.property.type.csv",
    ],
    # "demo": ["demo/estate_property_demo.xml", "demo/estate_property_offer_demo.xml"],
    "license": "AGPL-3",
}
