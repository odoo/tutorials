{  # noqa: B018
    "name": "Real Estate",
    "summary": """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,
    "description": """
        Real Estate module for "Server framework 101, chapter 2: A New Application"
    """,
    "author": "Dimitris Mystriotis",
    "website": "https://www.odoo.com/",
    "category": "Real Estate/Brokerage",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "website",
    ],
    "data": [
        "models/estate_property_type.xml",
        "models/estate_property_tag.xml",
        "models/estate_property.xml",
        "models/estate_property_offer.xml",
        "security/ir.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
        "controllers/estate_property.xml",
        "data/estate_tour.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/js/tour.js",
        ],
    },
    "license": "AGPL-3",
}
