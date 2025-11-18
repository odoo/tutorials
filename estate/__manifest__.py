#!/usr/bin/env python3
{
    "name": "Real Estate",
    "description": """
    Real Estate Module to Buy and Sell Your Real Estate with Ease.
    """,
    "version": "1.0",
    "depends": ["base"],
    "author": "danal",
    "category": "Category",
    "application": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
}
