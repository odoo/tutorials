#!/usr/bin/env python3
{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "danal",
    "category": "Category",
    "application": True,
    "license": "LGPL-3",
    "description": """
    Real Estate Module to Buy and Sell Your Real Estate with Ease.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
}
