{
    "name": "Real Estate",
    "description": " Make a fortune managing your real estate simply with Odoo",
    "version": "1.8",
    "category": "All",
    "sequence": 15,
    "summary": "Manage your residential opps",
    "depends": [
        "base_setup",
    ],
    "data": [
        "security/ir.model.access.csv",

        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
        "data/estate.property.type.csv",
    ],
    "demo": [

    ],
    "installable": True,
    "application": True,
    "auto_install": True,
    "assets": {},
    "license": "LGPL-3",
}
