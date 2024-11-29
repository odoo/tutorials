# -*- coding: utf-8 -*-
{
    "name": "Estate",
    "summary": """
        Tutorial starting module
    """,
    "description": """
        Tutorial starting module
    """,
    "author": "",
    "category": "Real Estate/Brokerage",
    "version": "0.1",
    "depends": ["base"],
    "application": True,
    "demo": [
        "demo/estate.property.type.csv",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_salesperson_views.xml",
        "views/estate_menus.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
    ],
    "license": "AGPL-3",
}
