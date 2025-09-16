# -*- coding: utf-8 -*-
{
    "name": "Estate Module",
    "summary": """
        TO BE DEF"
    """,
    "description": """
        TO BE DEF"
    """,
    # any module necessary for this one to work correctly
    "depends": ["base"],
    "application": True,
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/menus.xml",
    ],
}
