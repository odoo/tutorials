{
    "name": "estate",
    "version": "1.0",
    "summary": "Estate management",
    "description": "Estate management",
    "author": "Odoo S.A.",
    "website": "https://www.odoo.com/",
    "license": "LGPL-3",
    "category": "Uncategorized",
    "depends": ["base"],
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml"
    ],
}
