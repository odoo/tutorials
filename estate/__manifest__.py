{
    "name": "Real Estate",
    "version": "1.0",
    "category": "Real Estate",
    "summary": "Module to manage real estate advertisements",
    "description": "A module to create and manage real estate advertisements.",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_kanban.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml"
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
