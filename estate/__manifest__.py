{
    "name": "Estate",
    "license": "LGPL-3",
    "application": True,
    "summary": "Real-estate module for tutorial",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",

        "data/ir_sequence_data.xml",

        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_user_views.xml",

        "views/estate_menus.xml",
    ],
}
