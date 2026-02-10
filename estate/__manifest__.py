{
    "name": "Estate",
    "application": True,
    "description": "Specific Real Estate Module",
    "depends": ["base", "crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "author": "Maram-Odoo",
    "license": "LGPL-3",
}
