{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "Odoo SA",
    "category": "Accounting",
    "summary": "Helps manage real estate",
    "icon": "/estate/static/description/icon.png",
    "description": """
    Description text
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "demo": [
        "demo/demo.xml",
    ],
}
