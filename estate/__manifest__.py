{
    "name" : "estate",
    "summary" : "A real estate app",
    "version" : "0.1",
    "description" : "A real estate app developed by Mahavir Patel (pmah) within the four walls of Odoo IN",
    "author" : "Mahavir Patel (pmah)",
    "website" : "https://odoo.com",
    "category" : "Tutorials/Estate",
    "depends" : ["base"],
    "application" : True,
    "installable" : True,
    "maintainer" : "Mahavir Patel (pmah)",
    "license" : "LGPL-3",
    "data" : [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml"
    ]
}
