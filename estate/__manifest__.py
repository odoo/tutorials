{
    "name": "Real Estate",
    "author": "Odoo S.A.",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "application": True,
    "installable": True,
}
