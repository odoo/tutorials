{
    "name": "estate",
    "installable": True,
    "application": True,
    "category": "Real Estate/Brokerage",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/security.xml",
        "security/ir.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "data/estate.property.type.csv",
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    "author": "Weng Hou Mak (wemak)",
    "license": "LGPL-3",
}
