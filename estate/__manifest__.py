{
    "name": "Real Estate",
    "version": "1.1",
    "category": "Real Estate/Brokerage",
    "summary": "Manage Real Estate Properties, Sales, and Offers",
    "description": """ following my turorials on Odoo 18 Chapter 1 to 13 """,
    "author": "Kashish",
    "website": "https://www.google.com",
    "license": "LGPL-3",
    "icon": "/estate/static/description/icon.png",
    "depends": [
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
