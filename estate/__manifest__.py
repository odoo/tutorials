{
    "name": "Real Estate",
    "description": "",
    "category": "Real Estate/Brokerage",
    "depends": ["base"],
    "sequence": 1,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/css/custom.css",
        ],
    },
    "license": "LGPL-3",
    "application": True,
    "installable": True,
}
