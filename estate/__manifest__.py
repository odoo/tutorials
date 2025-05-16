{
    "name": "Estate",
    "application": True,
    "depends": ["base", "mail", "website"],
    "sequence": 1,
    "license": "LGPL-3",
    "installable": True,
    "category": "Real Estate/Brokerage",
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "reports/estate_property_templates.xml",
        "reports/estate_property_reports.xml",
        "views/estate_property_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_offer_views.xml",
        "views/estate_type_views.xml",
        "views/estate_menus.xml",
        "views/properties_website_template.xml"
    ],
    "demo": [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
    ],
}
