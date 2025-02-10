{
    "name": "estate",
    "version": "1.0",
    "author": "ksni-odoo",
    "depends": ["base"],
    "installable": True,
    "application": True,
    "data": [
        "data/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_users.xml",
        "views/estate_menus.xml",
    ],
}
