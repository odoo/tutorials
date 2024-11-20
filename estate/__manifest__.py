{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "djip-odoo",
    "description": """
        part of technical training
    """,
    "data": [
        "views/actions_menu_and_button.xml",
        "views/menu_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/estate.property.types.csv",
        "demo/estate.property.tags.csv",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offers_demo.xml"
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
