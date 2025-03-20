{
    "name": "estate",
    "version": "0.1",
    "description": """
  The Estate Module manages real estate properties, buyers, sellers, and offers efficiently.
    """,
    "depends": ["mail", "website"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tags_view.xml",
        "views/estate_menus.xml",
        "views/res_users_view.xml",
        "data/estate.property.type.csv",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml",
        "data/estate_property_menu.xml",
        "views/estate_property_templates.xml",
        "views/property_details.xml",
    ],
    "category": "Real Estate/Brokerage",
    "application": True,
    "license": "AGPL-3",
}
