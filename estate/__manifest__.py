{
    "name": "Estate Tutorial",
    "author": "joemo",
    "license": "LGPL-3",
    "application": True,
    "depends": ["base", "base_import_module", "website"],
    "data": [
        "models/estate_property_type.xml",
        "models/estate_property_tag.xml",
        "models/estate_property.xml",
        "models/estate_property_offer.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "controllers/estate_property_controllers.xml",
        "data/x_estate.property.type.csv",
    ]
}
