# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Real Estate Advertisement",
    "author": "Odoo",
    "category": "Sales/Real Estate",
    "sequence": 15,
    "summary": "Manage property listings and real estate advertisements",
    "description": """
Real Estate Advertisement Management
====================================
This module allows you to manage real estate properties, including:
    * Property listings with detailed information
    * Property types and tags
    * Property offers and negotiations
    * Sales tracking
    """,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/css/estate.css",
        ],
    },
    "application": True,
    "license": "LGPL-3",
}
