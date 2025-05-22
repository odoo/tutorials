{
    "name": "Real Estate",
    "category": "Real Estate/Brokerage",
    "depends": ["base"],
    "application": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "security/estate_security.xml",
        "data/estate.property.type.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
}
