{
    "name": "Real Estate",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_list_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menuitem.xml",
        "views/estate_property_offer_views.xml",
        "data/estate_property_type.xml",
        "data/estate_property_tag.xml",
        "data/estate_property_demo.xml",
    ],
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
