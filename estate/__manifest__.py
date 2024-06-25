{
    "name": "Real Estate",
    "version": "3.0",
    "depends": ["base", "web"],
    "category": "Real Estate/Brokerage",
    "license": "LGPL-3",
    "installable": True,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_sequence.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate.property.type.csv",
        "demo/demo.estate.property.xml",
        "demo/demo.estate.property.offer.xml",
    ],
}
