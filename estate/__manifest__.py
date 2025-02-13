{
    "name": "Estate",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_view.xml",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
        "data/master_data.xml",
    ],
    "demo":[
        "demo/demo_data.xml",
    ],
    "installable": True,
    "application": True,
}

