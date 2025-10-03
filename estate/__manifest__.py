{
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "application": True,
    "installable": True,
    "depends": ["base"],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "data/estate_property_type_data.xml",
        "views/estate_property_offers_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/estate_property_res_users_views.xml",
    ],
    "demo":[
        "demo/estate_property_demo.xml",
    ],
    "license": "LGPL-3",
}
