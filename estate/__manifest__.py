{
    "name": "Real Estate",
    "depends": ["base"],
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
    ],
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
