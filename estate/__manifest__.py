{
    "name": "estate",
    "summary": "A real estate app",
    "description": "A real estate app developed by Vedant within the four walls of Odoo IN",
    "author": "Vedant Pandey (vpan)",
    "website": "https://odoo.com",
    "category": "Tutorials/Estate",
    "version": "0.1",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_offers_views.xml",
        "views/estate_menus.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3"
}
