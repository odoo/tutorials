{
    "name": "estate",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    "author": "ksni-odoo",
    "depends": ["base","mail"],
    "installable": True,
    "application": True,
    "data": [
        "security/estate_groups.xml",
        "security/estate_property_security.xml",   
        "security/ir.model.access.csv",
        "data/estate.property.type.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_users.xml",
        "views/estate_menus.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/estate_property_template.xml"
    ],
    "demo": [
        "demo/estate.property.xml",
        "demo/estate.property.offer.xml"
    ],
    "license": "LGPL-3"
}
