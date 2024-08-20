{
    "name": "estate",
    "version": "0.1",
    "depends": ["base", "mail"],
    "description": "Technical practice",
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "data/estate.property.type.csv",
        "report/estate_property_templates.xml",
        "report/estate_property_report.xml",
        "views/res_user_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "license": "LGPL-3",
}
