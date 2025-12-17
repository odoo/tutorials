{
    "name": "estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "Odoo S.A.",
    "category": "Real Estate",
    "description": """
    Description text
    """,
    "application": True,
    "installable": True,
    "data": [
        "data/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type.xml",
        "views/estate_property_tag.xml",
        "views/estate_property_offer.xml",
        "views/estate_menus.xml",
    ],
}
