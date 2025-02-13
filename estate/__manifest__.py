{
    "name": "Real Estate",
    "description": "This is a real estate app",
    "application": True,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "view/estate_property_views.xml",
        "view/estate_property_offers_view.xml",
        "view/property_type_view.xml",
        "view/res_users_estate_view.xml",
        "view/estate_property_tags_view.xml",
        "view/estate_menus.xml",
    ],
    "license": "LGPL-3",
    "sequence": 1,
}
