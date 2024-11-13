{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "djip-odoo",
    "description": """
        part of technical training
    """,
    "data": [
        "views/menu_actions.xml",
        "views/menu_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_types_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offers_views.xml",
        
        "security/ir.model.access.csv",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
}
