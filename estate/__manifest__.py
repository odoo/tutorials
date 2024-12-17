{
    "name": "ESTATE",
    "version": "1.0",
    "category": "Real Estate/Brokerage",
    "summary": "Allow Users to Buy and Sell Property",
    "website": "https://www.odoo.com",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_users_views.xml",
        "views/estate_menus.xml",
        "data/estate_property_type_data.xml",
    ],
    "demo": [
        "demo/estate_property_demo_data.xml",
        "demo/estate_property_offer_demo_data.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
    "author": "Odoo",
}
