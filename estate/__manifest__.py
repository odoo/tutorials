{
    "name": "Real Estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/estate_security.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "data/estate_property_type_data.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_offer_templates.xml",
        "report/user_estate_property_template.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml"
    ],
    "demo": [
        "demo/estate_property_demo_data.xml",
        "demo/estate_property_offer_demo_data.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
    "category": "Real Estate/Brokerage"
}
