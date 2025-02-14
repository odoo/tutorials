{
    "name": "estate",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail"],  # Add 'mail' module
    "data": [
        "views/res_user_views.xml",
        "views/estate_property_offer.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "report/estate_property_template.xml",
        "report/estate_property_reports.xml",
        "report/res_users_template.xml",
        "report/res_users_reports.xml",
        "security/estate_security.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/estate_demo.xml"],
    "application": True,
}
