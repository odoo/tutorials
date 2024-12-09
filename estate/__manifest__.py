{
    "name": "ESTATE",
    "version": "1.0",
    "category": "Tutorials/Estate",
    "summary": "Allow Users to Buy and Sell Property",
    "website": "https://www.odoo.com",
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
    "author": "Odoo",
}
