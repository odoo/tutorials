{
    "name": "estate",
    "category": "Real Estate",
    "depends": ["base", "mail"],
    "application": True,
    "installable": True,
    "author": "Odoo S.A.",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offers.xml",
        "views/estate_property_types.xml",
        "views/estate_property_tags.xml",
        "views/estate_property.xml",
        "views/res_users.xml",
        "views/estate_property_menus.xml",
    ],
}
