{
    "name": "estate",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail"],  # Add 'mail' module
    "data": [
        "wizard/estate_property_offer_wizard_view.xml",
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
        "report/estate_property_mail_template.xml",
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_webpage.xml",
        "views/estate_property_webpage_property_detail.xml"
    ],
    "demo": ["demo/estate_demo.xml"],
    "application": True,
}
