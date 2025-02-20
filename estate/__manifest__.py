{
    "name": "estate",
    "version": "1.0",
    "license": "LGPL-3",
    "category":"Real Estate/Brokerage",
    "depends": ["base","mail","website"],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "data/estate.property.type.csv",
        "report/estate_report_views.xml",
        "report/estate_report.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/res_user.xml",
        "views/estate_menus.xml",
        "views/property_list_website_template.xml",
        "views/property_details_website_template.xml"
    ],
    "demo": [
        "demo/property_demo_data.xml",
        "demo/offer_demo_data.xml",
    ],
    "installable": True,
    "application": True,  # this makes the applications available even in app filter is on
    "auto-install": False,
}
