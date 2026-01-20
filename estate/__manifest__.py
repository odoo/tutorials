{
    "name": "Estate",
    "version": "1.9",
    "category": "Real Estate",
    "summary": "Manage your real estate properties",
    "author": "Odoo",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
}
