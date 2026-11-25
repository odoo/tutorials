{
    "name": "Real Estate",
    "category": "Tutorials",
    "summary": "Real Estate App",
    "installable": True,
    "application": True,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag.xml",
        "views/estate_property_maintenance.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "author": "Rohit Agarkar",
    "license": "LGPL-3",
}
