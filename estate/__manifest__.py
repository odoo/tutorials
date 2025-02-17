{
    "name": "estate",
    "sequence": 1,
    "category": "Real Estate/Brokerage",
    "description": "",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/estate.property.type.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_user_views.xml",
    ],
    "demo":[
        "demo/estate_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
