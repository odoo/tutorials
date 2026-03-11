{
    "name": "Real Estate",
    "version": "19.0.0",
    "category": "Tutorials",
    "depends": ["base", "web"],
    "author": "hemeh",
    "application": True,
    "summary": "Manage real estate properties",
    "description": """
    Manage real estate properties.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_meetings_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menus.xml",
        "views/res_users_view.xml",
        "demo/demo_data.xml",
    ],
    "website": "https://odoo.com",
    "license": "LGPL-3",
    "installable": True,

}
