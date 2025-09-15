# -*- coding: utf-8 -*-
{
    "name": "Real Estate",
    "version": "0.1",
    "depends": ["base"],
    "author": "Madhav Pancholi",
    "category": "Real Estate",
    "description": """
        Manage properties, rentals, and real estate sales.
    """,
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_menus.xml",
    ],
    "demo": [],
}
