{
    "name": "Real_estate",
    "version": "1.8",
    "category": "Real Estate/Brokerage", 
    "summary": "Track leads and close opportunities",
    "depends": [
        "base",
        "mail",
        "website",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        "data/estate.property.type.csv",
        "data/estate.property.demo.xml",
        "data/estate.property.offer.demo.xml",
        "data/website_menu.xml",

        "wizard/estate_offer_views.xml",

        "views/property_detail.xml",
        "views/property_listing.xml",
        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_offer_templates.xml",
        "report/estate_property_templates.xml",
        "report/res_user_templates.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
