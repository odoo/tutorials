{
    "name": "Real Estate",
    "author": "nmak",
    "website": "https://www.odoo.com/apps/estate",
    "category": "tutorials/real-estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
