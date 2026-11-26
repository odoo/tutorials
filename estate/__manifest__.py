{  # noqa: B018
    "name": "Estate App",
    "depends": ["base"],
    "data": [
        "security/ir.access.csv",
        # Keep before estate_property_type_views.xml
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "application": True,
    "author": "Odoo",
    "license": "LGPL-3",
}
