{
    "name": "Real_estate",
    "version": "1.8",
    'category': 'Real Estate/Brokerage', 
    "summary": "Track leads and close opportunities",
    "depends": [
        "base",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        "data/estate.property.type.csv",
        "data/estate.property.demo.xml",
        "data/estate.property.offer.demo.xml",

        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
