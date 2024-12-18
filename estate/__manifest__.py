{
    "name": "Real Estate",
    "author": "Odoo",
    "website": "https://www.odoo.com/",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
}
